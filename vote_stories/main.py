import asyncio
from vote_stories_agent import VoteStoriesAgent
from models import MODELS


async def main():
    """Main function"""
    try:
        agent = VoteStoriesAgent(llm=MODELS.get("NVIDIA_CHATGPT_OSS_20B_COMPLETIONS"))
        
        result = await agent.analyze("As a user, I want to be able to create a report in a click.")

        print(result)
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("\nTo fix this:")
        print("1. Create a .env file in the root directory")
        print("2. Add your NVIDIA API key: BUILD_NVIDIA_API_KEY=your_api_key_here")
        print("3. Get your API key from: https://build.nvidia.com/")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    asyncio.run(main())