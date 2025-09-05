import asyncio
from agents import Agent, OpenAIChatCompletionsModel, RunResult
from models import MODELS
from tools import get_story_score
from agents import set_tracing_disabled
from prompts import format_vote_stories_prompt
from agents import Runner
from state import VoteStoriesState


class VoteStoriesAgent:
    def __init__(self, llm=None):
        self.llm = llm
        self.tools = [get_story_score]

        # Check if API key is available
        if not MODELS.get("NVIDIA_CHATGPT_OSS_20B_COMPLETIONS"):
            raise ValueError("NVIDIA API key not found. Please set BUILD_NVIDIA_API_KEY in your .env file")

        self.agent = Agent(
            name="VoteStoriesAgent",
            instructions="You are a helpful assistant that will vote on a agile user story.",
            model=OpenAIChatCompletionsModel(
                model="openai/gpt-oss-20b",
                openai_client=MODELS["NVIDIA_CHATGPT_OSS_20B_COMPLETIONS"]
            ),
            #tools=self.tools,
        )

        set_tracing_disabled(disabled=True)

    async def analyze(self, story: str) -> str:
        """Run the vote stories analysis"""

        initial_state: VoteStoriesState = {
            "story": story,
            "arguments": ["However, the tradeoff between UX and security is a concern."],
        }

        try:
            result = await Runner.run(
                self.agent,
                format_vote_stories_prompt(initial_state),
            )

            return result.final_output

        except asyncio.TimeoutError:
            error_msg = "Request timed out after 30 seconds. The API might be slow or unresponsive."
            print(error_msg)
            return error_msg
        except Exception as e:
            error_msg = f"Error during analysis: {str(e)}"
            print(error_msg)
            return error_msg





