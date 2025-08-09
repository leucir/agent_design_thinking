from typing import Dict, Any


# Helper functions for state management
def add_answer(state: Dict[str, Any], answer: str) -> Dict[str, Any]:
    """Add a new answer to the state"""
    state["answers"].append(answer)
    state["current_answer"] = answer
    return state

def add_evaluation(state: Dict[str, Any], evaluation: Dict[str, Any]) -> Dict[str, Any]:
    """Add evaluation results to the state"""
    state["evaluations"].append(evaluation)
    if "quality_score" in evaluation:
        state["quality_scores"].append(evaluation["quality_score"])
    return state

def should_continue_iteration(state: Dict[str, Any]) -> bool:
    """Determine if iteration should continue based on state"""
    # Check max iterations
    if state["current_iteration"] >= state["max_iterations"]:
        state["stop_reason"] = "max_iterations_reached"
        return False
    
    # Check quality threshold
    if state["quality_scores"] and state["quality_scores"][-1] >= state["quality_threshold"]:
        state["stop_reason"] = "quality_threshold_met"
        return False
    
    # Check improvement threshold
    if len(state["quality_scores"]) >= 2:
        last_score = state["quality_scores"][-1]
        previous_score = state["quality_scores"][-2]
        if last_score - previous_score < state["improvement_threshold"]:
            state["stop_reason"] = "insufficient_improvement"
            return False
    
    # Check for errors
    if len(state["errors"]) > 0:
        state["stop_reason"] = "error_encountered"
        return False
    
    return True

def increment_iteration(state: Dict[str, Any]) -> Dict[str, Any]:
    """Increment the iteration counter"""
    state["current_iteration"] += 1
    state["retry_count"] = 0  # Reset retry count for new iteration
    return state