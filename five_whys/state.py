from typing import TypedDict, List, Dict, Any, Annotated
from langchain_core.messages import BaseMessage
from structure_outputs import WebSearchOutput

class FiveWhysState(TypedDict):

    """State for 5 Whys analysis"""
    # Core problem
    problem_statement: str
    current_focus: str
    
    # 5 Whys chain
    current_why_level: int
    max_why_levels: int
    why_questions: List[str]
    why_answers: List[str]
    why_chain: List[Dict[str, Any]]
    
    # Web search
    web_search_results: WebSearchOutput

    # Analysis components
    assumptions_made: List[str]
    evidence_needed: List[str]
    evidence_gathered: List[str]
    
    # Quality metrics
    depth_scores: List[float]
    relevance_scores: List[float]
    actionability_scores: List[float]
    
    # Validation and refinement
    validation_results: List[Dict[str, Any]]
    refinement_suggestions: List[str]
    
    # Solutions
    potential_solutions: List[str]
    recommended_actions: List[str]
    solution_details: Dict[str, Any]
    
    # Final results
    final_root_cause: str
    final_report: str
    
    # Control
    should_continue: bool
    stop_reason: str


    # Debugging & Monitoring
    processing_time: float
    node_history: List[str]
    
    # Error handling
    errors: List[str]