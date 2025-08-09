from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, SystemMessage, HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langgraph.graph import StateGraph, START, END

from prompts import (
    CLARIFICATION_PROMPT, 
    format_cause_analysis_prompt, 
    format_why_question_prompt, 
    format_validation_prompt, 
    format_solution_prompt,
    format_why_question_prompt,
    format_report_prompt,
    format_why_question_chain_prompt
)

from structure_outputs import CauseAnalysisOutput, ValidationOutput, SolutionOutput
from models import MODELS
from state import FiveWhysState
from typing import Dict, Any, List, Literal
import json
import time
from tools import web_search
from config import agent_config


"""
Five Whys Agent

This agent is a simple agent that uses the five whys method to answer a question.

"""

class FiveWhysAgent:

    def __init__(self, llm=None):
        self.llm = llm
        self.graph = self._build_graph()

    def _build_graph(self):
        """Build the LangGraph for 5 Whys analysis"""
        
        # Create the graph
        workflow = StateGraph(FiveWhysState)
        
        # Add nodes
        workflow.add_node("entry", self.entry_node)
        workflow.add_node("why_question", self.why_question_node)
        workflow.add_node("web_search_cause_analysis", self.web_search_cause_analysis_node)
        workflow.add_node("cause_analysis", self.cause_analysis_node)
        workflow.add_node("validation", self.validation_node)
        workflow.add_node("decision", self.decision_node)
        workflow.add_node("solution_generation", self.solution_generation_node)
        workflow.add_node("synthesis", self.synthesis_node)
        workflow.add_node("error_handling", self.error_handling_node)
        
        # Define the flow
        workflow.set_entry_point("entry")
        
        # Entry -> Why Question
        workflow.add_edge("entry", "why_question")
        
        # Why Question -> Cause Analysis
        workflow.add_edge("why_question", "web_search_cause_analysis")

        # Web Search Cause Analysis -> Cause Analysis
        workflow.add_edge("web_search_cause_analysis", "cause_analysis")

        # Cause Analysis -> Validation (or Error Handling)
        workflow.add_conditional_edges(
            "cause_analysis",
            self.route_after_cause_analysis,
            {
                "validation": "validation",
                "error_handling": "error_handling"
            }
        )
        
        # Validation -> Decision
        workflow.add_edge("validation", "decision")
        
        # Decision -> Continue or Stop
        workflow.add_conditional_edges(
            "decision",
            self.route_after_decision,
            {
                "continue": "why_question",
                "solution_generation": "solution_generation"
            }
        )
        
        # Solution Generation -> Synthesis
        workflow.add_edge("solution_generation", "synthesis")
        
        # Error Handling -> Decision or End
        workflow.add_conditional_edges(
            "error_handling",
            self.route_after_error,
            {
                "retry": "cause_analysis",
                "end": END
            }
        )
        
        # Synthesis -> End
        workflow.add_edge("synthesis", END)
        
        return workflow.compile()


    def entry_node(self, state: FiveWhysState) -> FiveWhysState:
        """Initialize the 5 Whys analysis"""

        state["node_history"].append("entry")
        state["processing_time"] = time.time()
        
        # Parse and clarify the problem statement
        clarification_prompt = CLARIFICATION_PROMPT

        messages = [
            SystemMessage(content=clarification_prompt),
            HumanMessage(content=f"Problem: {state['problem_statement']}")
        ]
        
        response = self.llm.invoke(messages)
        
        try:
            clarification = json.loads(str(response.content))
            state["problem_statement"] = clarification.get("clarified_problem", state["problem_statement"])
            state["assumptions_made"] = clarification.get("assumptions", [])
            state["evidence_needed"] = clarification.get("evidence_needed", [])
        except json.JSONDecodeError:
            state["problem_statement"] = state["problem_statement"]
        
        # Initialize first "why"
        state["current_focus"] = state["problem_statement"]
        
        return state



    def why_question_node(self, state: FiveWhysState) -> FiveWhysState:
        """Generate the next 'why' question"""
        state["node_history"].append("why_question")
        
        current_level = state["current_why_level"]
        
        if current_level == 0:
            # First why - ask why the problem occurs
            why_question = format_why_question_prompt(dict(state))
        else:
            # Subsequent whys - ask why the previous cause occurs
            why_question = format_why_question_chain_prompt(dict(state))
        
        state["why_questions"].append(why_question)
        state["current_why_level"] += 1
        
        return state



    def cause_analysis_node(self, state: FiveWhysState) -> FiveWhysState:
        """Analyze and identify the cause for the current why question"""
        state["node_history"].append("cause_analysis")
        
        current_question = state["why_questions"][-1]
        
        analysis_prompt = format_cause_analysis_prompt(dict(state), current_question)
        
        messages = [
            SystemMessage(content=analysis_prompt),
            HumanMessage(content=current_question),
        ]

        model_with_structure = self.llm.with_structured_output(CauseAnalysisOutput)

        response = model_with_structure.invoke(messages)
        
        try:

            analysis = json.loads(str(CauseAnalysisOutput.model_dump_json(response)))
            
            # Store the primary cause
            primary_cause = analysis.get("primary_cause", "Unknown cause")
            state["why_answers"].append(primary_cause)
            
            # Store the question-answer pair
            state["why_chain"].append({
                "question": current_question,
                "answer": primary_cause,
                "evidence": analysis.get("evidence", ""),
                "alternatives": analysis.get("alternative_causes", []),
                "level": state["current_why_level"]
            })
            
            # Store quality metrics
            confidence = analysis.get("confidence_level", 0.5)
            state["depth_scores"].append(confidence)
            
            # Store evidence
            if analysis.get("evidence"):
                state["evidence_gathered"].append(analysis["evidence"])
            
            # Update current focus
            state["current_focus"] = primary_cause
            
        except json.JSONDecodeError:
            state["errors"].append("Failed to parse cause analysis response")
        
        return state


    def web_search_cause_analysis_node(self, state: FiveWhysState) -> FiveWhysState:
        """Web search for cause analysis"""
        state["node_history"].append("web_search_cause_analysis")
        

        #Not sure if I use the last question or the current focus, such as the topic of the question
        current_question = state["why_questions"][-1]
        
        #execute web search, using the current question as the query
        web_search_result = web_search(current_question)
        
        #store the web search result in the state
        state["web_search_results"] = web_search_result
                
        return state


    def validation_node(self, state: FiveWhysState) -> FiveWhysState:
        """Validate the current cause and the overall chain"""
        state["node_history"].append("validation")
        
        validation_prompt = format_validation_prompt(dict(state))
        
        messages = [
            SystemMessage(content=validation_prompt),
            HumanMessage(content="Please validate the current 5 Whys chain.")
        ]
        
        model_with_structure = self.llm.with_structured_output(ValidationOutput)
        response = model_with_structure.invoke(messages)
        
        try:
            validation = json.loads(str(ValidationOutput.model_dump_json(response)))
            state["validation_results"].append(validation)
            
            # Store suggestions for improvement
            if validation.get("improvement_suggestions"):
                state["refinement_suggestions"].extend(validation["improvement_suggestions"])
            
            # Update quality scores
            if validation.get("chain_validity"):
                state["relevance_scores"].append(validation["chain_validity"])
            
            if validation.get("actionability"):
                state["actionability_scores"].append(validation["actionability"])
            
        except json.JSONDecodeError:
            state["errors"].append("Failed to parse validation response")
        
        return state


    
    def decision_node(self, state: FiveWhysState) -> FiveWhysState:
        """Decide whether to continue the 5 Whys process"""
        state["node_history"].append("decision")
        
        should_continue = True
        stop_reason = ""
        
        # Check if we've reached max whys
        if state["current_why_level"] >= state["max_why_levels"]:
            should_continue = False
            stop_reason = "max_whys_reached"
        
        # Check if we've found a likely root cause
        elif state["validation_results"]:
            latest_validation = state["validation_results"][-1]
            if latest_validation.get("is_root_cause_likely", False):
                should_continue = False
                stop_reason = "root_cause_identified"
        
        # Check if we're not making progress (low depth scores)
        elif len(state["depth_scores"]) >= 2:
            recent_scores = state["depth_scores"][-2:]
            if all(score < 0.3 for score in recent_scores):
                should_continue = False
                stop_reason = "insufficient_depth"
        
        state["should_continue"] = should_continue
        state["stop_reason"] = stop_reason
        
        return state



    def solution_generation_node(self, state: FiveWhysState) -> FiveWhysState:
        """Generate potential solutions based on the identified root causes"""
        state["node_history"].append("solution_generation")
        
        solution_prompt = format_solution_prompt(dict(state))
        
        messages = [
            SystemMessage(content=solution_prompt),
            HumanMessage(content="Generate solutions based on the 5 Whys analysis.")
        ]
        
        model_with_structure = self.llm.with_structured_output(SolutionOutput)
        response = model_with_structure.invoke(messages)
        
        try:
            solutions = json.loads(str(SolutionOutput.model_dump_json(response)))
            state["potential_solutions"] = solutions.get("immediate_actions", [])
            state["recommended_actions"] = solutions.get("preventive_measures", [])
            state["solution_details"] = solutions
            
        except json.JSONDecodeError:
            state["errors"].append("Failed to parse solution response")
        
        return state



    def synthesis_node(self, state: FiveWhysState) -> FiveWhysState:
        """Create the final 5 Whys analysis report"""
        state["node_history"].append("synthesis")
        
        # Identify the root cause
        if state["why_chain"]:
            state["final_root_cause"] = state["why_chain"][-1]["answer"]
        
        # Create comprehensive report
        report_prompt = format_report_prompt(dict(state))

        messages = [
            SystemMessage(content=report_prompt),
            HumanMessage(content="Generate the final 5 Whys analysis report.")
        ]
        
        response = self.llm.invoke(messages)
        state["final_report"] = str(response.content)
        
        # Calculate processing time
        state["processing_time"] = time.time() - state["processing_time"]
        
        return state

    def error_handling_node(self, state: FiveWhysState) -> FiveWhysState:
        """Handle errors and decide recovery strategy"""
        state["node_history"].append("error_handling")
        
        if len(state["errors"]) > 3:
            state["should_continue"] = False
            state["stop_reason"] = "too_many_errors"
        
        return state


    # Routing functions
    def route_after_cause_analysis(self, state: FiveWhysState) -> Literal["validation", "error_handling"]:
        """Route after cause analysis"""
        if state["errors"]:
            return "error_handling"
        return "validation"


    def route_after_decision(self, state: FiveWhysState) -> str:
        """Route after decision node"""
        if state["should_continue"]:
            return "continue"
        else:
            return "solution_generation"


    def route_after_validation(self, state: FiveWhysState) -> str:
        """Route after validation"""
        if state["validation_results"]:
            latest = state["validation_results"][-1]
            recommended_action = latest.get("recommended_action", "continue")
            
            if recommended_action == "dig_deeper":
                return "why_question"
            elif recommended_action == "explore_alternatives":
                return "cause_analysis"  # Re-analyze current level
            else:
                return "decision"

        return "decision"


    def route_after_error(self, state: FiveWhysState) -> Literal["retry", "end"]:
        """Route after error handling"""
        if state["should_continue"]:
            return "retry"
        return "end"


    # Main interface
    def analyze(self, problem: str, max_whys: int = 5) -> Dict[str, Any]:
        """Run the 5 Whys analysis"""
        
        # Create initial state
        initial_state: FiveWhysState = {
            "problem_statement": problem,
            "final_root_cause": "",
            "final_report": "",
            "current_why_level": 0,
            "max_why_levels": max_whys,
            "why_questions": [],
            "why_answers": [],
            "why_chain": [],
            "depth_scores": [],
            "relevance_scores": [],
            "actionability_scores": [],
            "validation_results": [],
            "refinement_suggestions": [],
            "potential_solutions": [],
            "recommended_actions": [],
            "solution_details": {},
            "should_continue": True,
            "stop_reason": "",
            "current_focus": "",
            "evidence_gathered": [],
            "assumptions_made": [],
            "evidence_needed": [],
            "node_history": [],
            "processing_time": 0.0,
            "errors": []
        }
        
        # Run the analysis
        result = self.graph.invoke(
            initial_state, 
            config = 
                { "recursion_limit" : agent_config["graph"]["graph_recursion_limit"] }
        )
        
        return {
            "problem": result["problem_statement"],
            "root_cause": result["final_root_cause"],
            "why_chain": result["why_chain"],
            "solutions": result["potential_solutions"],
            "report": result["final_report"],
            "processing_time": result["processing_time"],
            "stop_reason": result["stop_reason"],
            "errors": result["errors"]
        }