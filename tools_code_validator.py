"""
title: Code Validator & Syntax Checker
author: copilot
description: Validate Python code syntax, check for common issues, and verify AST structure.
version: 1.0.0
license: MIT
"""

import ast
import re
from typing import List, Dict, Any, Optional

class Tools:
    def __init__(self):
        pass

    def validate_python(self, code: str) -> str:
        """
        Validate Python code for syntax errors and return AST structure info.
        :param code: Python source code to validate.
        :return: Validation result with functions, classes, and imports found.
        """
        try:
            tree = ast.parse(code)
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
            classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
            imports = []
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imports.append("import " + node.names[0].name)
                elif isinstance(node, ast.ImportFrom):
                    imports.append(f"from {node.module} import ...")

            result = "✅ Syntax valid.\n"
            if classes:
                result += f"Classes: {', '.join(classes)}\n"
            if functions:
                result += f"Functions: {', '.join(functions)}\n"
            if imports:
                result += f"Imports: {', '.join(imports)}\n"
            return result
        except SyntaxError as e:
            return f"❌ Syntax error at line {e.lineno}: {e.msg}\nText: {e.text}"

    def check_type_hints(self, code: str) -> str:
        """
        Check if functions have type hints and report missing ones.
        :param code: Python source code to analyze.
        :return: Report of functions with and without type hints.
        """
        try:
            tree = ast.parse(code)
            hinted = []
            missing = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    has_returns = node.returns is not None
                    has_args = all(
                        arg.annotation is not None
                        for arg in node.args.args
                        if arg.arg != 'self'
                    )
                    if has_returns and has_args:
                        hinted.append(node.name)
                    else:
                        missing.append(node.name)

            result = "Type Hint Analysis:\n"
            if hinted:
                result += f"  ✅ Full hints: {', '.join(hinted)}\n"
            if missing:
                result += f"  ⚠️  Missing hints: {', '.join(missing)}\n"
            return result
        except SyntaxError as e:
            return f"Cannot analyze: syntax error at line {e.lineno}"

    def count_loc(self, code: str) -> str:
        """Count lines of code, blanks, and comments."""
        lines = code.split('\n')
        total = len(lines)
        blanks = sum(1 for l in lines if not l.strip())
        comments = sum(1 for l in lines if l.strip().startswith('#'))
        code_lines = total - blanks - comments

        return f"Total: {total} | Code: {code_lines} | Comments: {comments} | Blank: {blanks}"