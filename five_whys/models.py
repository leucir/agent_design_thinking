from langchain_openai import ChatOpenAI, OpenAI
from langsmith.wrappers import wrap_openai
from dotenv import load_dotenv

import os

# Load environment variables from .env file
load_dotenv()

"""
Embedding Models
"""
EMBEDDING_MODEL_ID = "text-embedding-nomic-embed-text-v1.5"



"""
Environment Variables - Load from .env file
Note: Make sure to create a .env file in the root directory with the following variables:
- OPENAI_API_KEY
- LANGSMITH_TRACING
- LANGSMITH_PROJECT  
- LANGSMITH_ENDPOINT
- LANGSMITH_API_KEY
- TAVILY_API_KEY
"""

"""
Chat Models
"""

MODELS = {
    "LMSTUDIO_PHI3": 
        ChatOpenAI(
            model="microsoft/phi-4-reasoning-plus",
            api_key="PLACEHOLDER",
            base_url="http://127.0.0.1:1234/v1",
            streaming=False,
            temperature=0.8,
        ),
    "LMSTUDIO_PHI4": 
        OpenAI(
            model="microsoft/phi-4-reasoning-plus",
            api_key="PLACEHOLDER",
            base_url="http://127.0.0.1:1234/v1",
            streaming=False,
            temperature=0.8,
            max_tokens=2000,
        ),
    "PUBLIC_OPENAI_GPT4O":
        ChatOpenAI(
            model="gpt-4o",
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://api.openai.com/v1",
            streaming=False,
        ),
}

