from tavily import TavilyClient
import os
from structure_outputs import WebSearchOutput
import json
from config import enable_debug, agent_config

def extract_content_from_results(results_data):
    """
    Extract content from search results.
    
    Args:
        results_data: Dictionary containing search results
        
    Returns:
        List of content strings from the results
    """
    results = results_data.get('results', [])

    #only get the content of the results that are above the score threshold but cannot be more than the max results
    filtered_results = []
    for item in results:
        if item.get('score', 0) >= agent_config["tools"]["web_search"]["score_threshold"]:
            if len(filtered_results) < agent_config["tools"]["web_search"]["max_results"]:
                filtered_results.append(item)
            else:
                break

    if (enable_debug["DEBUG"]):
        print("Result web search after filtering", json.dumps(filtered_results, indent=4))

    return [item.get('content', '') for item in filtered_results]

def web_search(query: str) -> WebSearchOutput:
    """Searches the web using Tavily's API"""

    client = TavilyClient(
        api_key=os.getenv("TAVILY_API_KEY")
    )

    result = client.search(
        query=query[:agent_config["tools"]["web_search"]["max_query_length"]],  #truncate the query if it is too long
        search_depth=agent_config["tools"]["web_search"]["advanced_search"],
        max_results=agent_config["tools"]["web_search"]["max_results"]
    )

    return WebSearchOutput(
        search_results=extract_content_from_results(result),
        search_query=query,
        search_time=result.get('search_time', ''),
        search_engine=result.get('search_engine', ''),
        search_url=result.get('search_url', '')
    )
