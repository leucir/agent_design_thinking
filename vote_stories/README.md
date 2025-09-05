# Vote Stories Agent

This agent will receive content about a project, including job stories.
With that information, the agent will score each story with points (from 1 to 5) using a set of different arguments.
The set of arguments is not defined yet.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r ../requirements.txt
   ```

2. **Set up API key:**
   - Create a `.env` file in the root directory of the project
   - Add your NVIDIA API key:
     ```
     BUILD_NVIDIA_API_KEY=your_nvidia_api_key_here
     ```
   - Get your API key from: https://build.nvidia.com/

3. **Run the agent:**
   ```bash
   python main.py
   ```

## Troubleshooting

### Program hangs or gets stuck
- **Missing API key:** Make sure you have set the `BUILD_NVIDIA_API_KEY` in your `.env` file
- **Network issues:** The program now has a 30-second timeout to prevent infinite hanging
- **API rate limits:** NVIDIA's API might be slow or have rate limits

### Error messages
- If you see "NVIDIA API key not found", create a `.env` file with your API key
- If you see timeout errors, the API might be slow - try running again
- For other errors, check the console output for specific error messages

## Features

- **Timeout handling:** 30-second timeout to prevent hanging
- **Error handling:** Graceful error messages for common issues
- **API key validation:** Checks for required API keys before making requests
