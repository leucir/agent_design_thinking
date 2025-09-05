
agent_config = {

    "node": {
        "cause_analysis": {
            "use_web_search": True,
        }
    },
    "tools": {
        "web_search": {
            "score_threshold": 0.20,
            "advanced_search": "advanced", # basic or advanced
            "max_results": 3, # max number of results to return
            "max_query_length": 400, # max number of characters to query
        }
    },
    "graph": {
        "graph_recursion_limit": 30,
    }
}


enable_debug = {
    "DEBUG": False
}