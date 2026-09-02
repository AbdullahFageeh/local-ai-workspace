"""
title: Web Search (DuckDuckGo)
author: open-webui-community
description: Search the live web using DuckDuckGo to provide real-time information to all models.
version: 1.0.0
license: MIT
"""

from duckduckgo_search import DDGS
from typing import Callable, Any

class Tools:
    def __init__(self):
        pass

    def search_web(self, query: str) -> str:
        """
        Search the live web for current information, facts, or documentation using DuckDuckGo.
        :param query: The search term or question to look up.
        :return: Concise snippets and links from the top web results.
        """
        try:
            results = []
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=5):
                    title = r.get("title", "")
                    body = r.get("body", "")
                    href = r.get("href", "")
                    results.append(f"Title: {title}\nSnippet: {body}\nSource: {href}")
            
            if not results:
                return "No web results found for this query."
            
            return "\n\n---\n\n".join(results)
        except Exception as e:
            return f"Error executing web search: {str(e)}"
