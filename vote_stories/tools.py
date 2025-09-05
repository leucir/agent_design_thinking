from agents import function_tool
import random

@function_tool
def get_story_score(story: str) -> int:
    """
    Get the score of a story.
    """
    return random.randint(1, 5) # TODO: Implement the logic to score the story

