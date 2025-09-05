



VOTE_STORIES_PROMPT = """
You are a helpful assistant that will vote on a story.
You will be given a story and a set of arguments.
You will need to vote on the story based on the arguments.

The story is: {story}
The arguments are: {arguments}

Provide your vote in the following format. Vote is between 0 (WEAK) to 5 (GOOD).

"""


def format_vote_stories_prompt(state: dict) -> str:
    """
    Format the VOTE_STORIES_PROMPT template with provided state.
    """
    return VOTE_STORIES_PROMPT.format(
        story=state['story'],
        arguments=state['arguments']
    )