from langchain_openai import OpenAI
from openai import AsyncOpenAI

from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

"""
Environment Variables - Load from .env file
Note: Make sure to create a .env file in the root directory with the following variables:
- BUILD_NVIDIA_API_KEY
"""

NVIDIA_API_KEY = os.getenv("BUILD_NVIDIA_API_KEY")

# Check if API key is available
if not NVIDIA_API_KEY:
    print("Warning: BUILD_NVIDIA_API_KEY not found in environment variables.")
    print("Please create a .env file with your NVIDIA API key:")
    print("BUILD_NVIDIA_API_KEY=your_api_key_here")

MODELS = {}

if NVIDIA_API_KEY:
    MODELS.update({
        "NVIDIA_CHATGPT_OSS_20B": 
            OpenAI(
                model="openai/chatgpt-oss-20b",
                base_url="https://integrate.api.nvidia.com/v1",
            ),
        "NVIDIA_CHATGPT_OSS_20B_COMPLETIONS":
            AsyncOpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=NVIDIA_API_KEY,
            ),
    })
else:
    print("NVIDIA models not available due to missing API key")