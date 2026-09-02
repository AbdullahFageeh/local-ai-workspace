"""
title: URL Reader & Scraper
author: open-webui-community
description: Fetch web pages and clean HTML content into plain text for models to read and summarize.
version: 1.0.0
license: MIT
"""

import urllib.request
from bs4 import BeautifulSoup

class Tools:
    def __init__(self):
        pass

    def read_url(self, url: str) -> str:
        """
        Fetch and parse the readable text content of any public URL or webpage.
        :param url: The full web address (e.g. 'https://example.com').
        :return: Extracted plain text content from the webpage.
        """
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8', errors='ignore')
            
            soup = BeautifulSoup(html, 'html.parser')
            # Strip scripts, styles, and navigation bars
            for element in soup(["script", "style", "nav", "footer", "header"]):
                element.decompose()
            
            text = ' '.join(soup.stripped_strings)
            # Truncate to reasonable context window (~4000 characters)
            if len(text) > 4000:
                text = text[:4000] + "\n\n...[Content truncated for length]..."
            return text
        except Exception as e:
            return f"Error reading URL: {str(e)}"
