"""
title: Workspace Code Search
author: copilot
description: Search the local workspace for code patterns, filenames, and symbols using grep and file glob matching.
version: 1.0.0
license: MIT
"""

import os
import re
from typing import List, Dict, Any

class Tools:
    def __init__(self):
        self.workspace_root = os.environ.get("WORKSPACE_ROOT", os.path.expanduser("~"))

    def search_code(self, query: str, include_pattern: str = "**/*.py", case_sensitive: bool = False) -> str:
        """
        Search for text patterns in files across the workspace.
        :param query: The string or regex pattern to search for.
        :param include_pattern: Glob pattern to filter files (default: Python files).
        :param case_sensitive: Whether the search is case-sensitive.
        :return: Matching results with file paths and line content.
        """
        results = []
        flags = 0 if case_sensitive else re.IGNORECASE

        try:
            for root, dirs, files in os.walk(self.workspace_root):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', '__pycache__', 'venv', '.git')]

                for fname in files:
                    filepath = os.path.join(root, fname)
                    rel_path = os.path.relpath(filepath, self.workspace_root)

                    if include_pattern and not self._glob_match(rel_path, include_pattern):
                        continue

                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            for line_num, line in enumerate(f, 1):
                                if re.search(query, line, flags):
                                    results.append(f"{rel_path}:{line_num}: {line.strip()}")
                                    if len(results) >= 50:
                                        results.append("[...truncated, too many results]")
                                        break
                    except (PermissionError, UnicodeDecodeError):
                        pass
                if len(results) >= 50:
                    break

            if not results:
                return f"No matches found for '{query}' in {include_pattern}."
            return "\n".join(results)

        except Exception as e:
            return f"Search error: {str(e)}"

    def find_files(self, pattern: str) -> str:
        """
        Find files matching a glob pattern in the workspace.
        :param pattern: Glob pattern to match (e.g., '**/*.py', 'src/**/*.js').
        :return: List of matching file paths.
        """
        matches = []
        try:
            for root, dirs, files in os.walk(self.workspace_root):
                dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', '__pycache__', 'venv', '.git')]

                for fname in files:
                    filepath = os.path.join(root, fname)
                    rel_path = os.path.relpath(filepath, self.workspace_root)
                    if self._glob_match(rel_path, pattern):
                        matches.append(rel_path)

            if not matches:
                return f"No files matching '{pattern}'."
            return "\n".join(sorted(matches))

        except Exception as e:
            return f"File search error: {str(e)}"

    def _glob_match(self, path: str, pattern: str) -> bool:
        """Simple glob matching for common patterns."""
        regex = pattern.replace("**/", ".*").replace("**", ".*").replace("*", "[^/]*").replace("?", "[^/]")
        regex = "^" + regex + "$"
        return bool(re.match(regex, path))