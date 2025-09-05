


import json

SYSTEM_PROMPT = """

"""


CLARIFICATION_PROMPT = """
You are starting a 5 Whys root cause analysis. The user has provided a problem statement.
Your task is to:
1. Clarify and rephrase the problem statement to be specific and actionable
2. Identify any assumptions that need to be validated
3. Suggest what evidence or data might be helpful

"""


def format_clarification_prompt(state: dict) -> str:
    """
    Format the CLARIFICATION_PROMPT template with provided state.
    """
    return CLARIFICATION_PROMPT.format(state=state)



WHY_QUESTION_CHAIN_PROMPT = """
The original problem is {problem_statement}.
The last potential cause is identified as: {current_cause}.

Respond with a single question on why the last potential cause occurs.
"""


def format_why_question_chain_prompt(state: dict) -> str:
    """
    Format the WHY_QUESTION_CHAIN_PROMPT template with provided state.
    """
    return WHY_QUESTION_CHAIN_PROMPT.format(
        problem_statement=state['problem_statement'],
        current_cause=state['why_answers'][-1]
    )
WHY_QUESTION_PROMPT = """
Why does this problem occur: {problem_statement}?
"""


def format_why_question_prompt(state: dict) -> str:
    """
    Format the WHY_QUESTION_PROMPT template with provided state.
    """
    return WHY_QUESTION_PROMPT.format(problem_statement=state['problem_statement'])



CAUSE_ANALYSIS_PROMPT = """

You are conducting a 5 Whys root cause analysis. 

Problem Context: {problem_statement}
Previous Why Chain: {why_chain}
Current Question: {current_question}


Your task is to:
1. Identify the most likely cause that answers the current question
2. Provide evidence or reasoning for this cause
3. Consider if there are alternative causes
4. Assess how deep this cause goes (is it a symptom or root cause?)

"""


def format_cause_analysis_prompt(state: dict, current_question: str) -> str:
    """
    Format the CAUSE_ANALYSIS_PROMPT template with provided state and current question.
    
    Args:
        state: Dictionary containing problem_statement and why_chain
        current_question: The current why question being analyzed
        
    Returns:
        Formatted prompt string
    """
    return CAUSE_ANALYSIS_PROMPT.format(
        problem_statement=state['problem_statement'],
        why_chain=state['why_chain'],
        current_question=current_question,
        web_search_results=state['web_search_results']
    )


VALIDATION_PROMPT = """
        You are validating a 5 Whys analysis chain. Review the current chain and assess:
        
        Problem: {problem_statement}
        Current Why Chain: {why_chain_json}
        
        Validate:
        1. Logical consistency - does each why logically follow from the previous?
        2. Depth adequacy - are we getting to root causes or stuck on symptoms?
        3. Evidence strength - is there sufficient evidence for each cause?
        4. Actionability - can we act on the identified causes?
    """


def format_validation_prompt(state: dict) -> str:
    """
    Format the VALIDATION_PROMPT template with provided state.
    """
    return VALIDATION_PROMPT.format(
        problem_statement=state['problem_statement'],
        why_chain_json=json.dumps(state['why_chain'], indent=2)
    )




SOLUTION_PROMPT = """
        Based on the 5 Whys analysis, generate actionable solutions.
        
        Problem: {problem_statement}
        Root Cause Chain: {why_chain_json}
        
        Generate:
        1. Immediate actions to address the root cause
        2. Preventive measures to avoid recurrence
        3. Monitoring strategies to track effectiveness
        4. Alternative approaches if the primary solution fails
        """


def format_solution_prompt(state: dict) -> str:
    """
    Format the SOLUTION_PROMPT template with provided state.
    """
    return SOLUTION_PROMPT.format(
        problem_statement=state['problem_statement'],
        why_chain_json=json.dumps(state['why_chain'], indent=2)
    )



REPORT_PROMPT = """
        Create a comprehensive 5 Whys analysis report.
        
        Problem: {problem_statement}
        Analysis Chain: {why_chain_json}
        Solutions: {solutions_json}
        
        Create a structured report with:
        1. Executive summary
        2. Problem analysis
        3. Root cause identification
        4. Recommended actions
        5. Implementation plan
        """


def format_report_prompt(state: dict) -> str:
    """
    Format the REPORT_PROMPT template with provided state.
    """
    return REPORT_PROMPT.format(
        problem_statement=state['problem_statement'],
        why_chain_json=json.dumps(state['why_chain'], indent=2),
        solutions_json=json.dumps(state.get('solution_details', {}), indent=2)
    )

