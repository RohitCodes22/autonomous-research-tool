# The eyes of the program. 
# Takes a query string and returns structured JSON data
# Connects to SerpAPI and returns search results

import requests # For making HTTP requests
import json
from typing import Dict, Any 
from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

load_dotenv()
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

def web_search(query: str) -> Dict[str, Any]:
    params = {
        "q": query,
        "api_key": SERPAPI_API_KEY,
        "engine": "google",
        "num": 5
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    return results