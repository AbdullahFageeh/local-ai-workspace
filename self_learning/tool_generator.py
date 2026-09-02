"""
Autonomous Tool Generator (Inspired by soulfir/miguel and cogitator-ai/self-modifying).
Detects missing capabilities, generates Python tool code, AST-validates, and saves it.
"""

import ast
import os
import sys
from typing import Dict, Any, Optional
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage

GENERATED_TOOLS_DIR = os.path.join(os.path.dirname(__file__), "generated_tools")
llm_synthesizer = ChatOllama(model="coder-architect:latest", temperature=0.1)

TOOL_SYNTHESIS_PROMPT = """You are an Autonomous Tool Synthesizer.
Write a clean, self-contained Python function with docstrings, type hints, and error handling.
Do NOT use external network libraries. Use standard library or pre-installed packages (math, hashlib, datetime, re, os).

Output ONLY pure Python code without markdown ticks or explanation.

Task: {task}
Tool Name: {tool_name}
"""

def validate_python_code(code_str: str) -> bool:
    """AST syntax validator to prevent code corruption (from Miguel safety rules)."""
    try:
        ast.parse(code_str)
        return True
    except SyntaxError as e:
        print(f"Syntax validation failed: {e}")
        return False

def synthesize_and_register_tool(tool_name: str, task_description: str) -> Optional[str]:
    """Generates, tests, and saves a new tool file."""
    prompt = TOOL_SYNTHESIS_PROMPT.format(tool_name=tool_name, task=task_description)
    response = llm_synthesizer.invoke([HumanMessage(content=prompt)])
    code = response.content.strip()
    
    # Strip any accidental markdown formatting
    if code.startswith("```python"):
        code = code[9:]
    if code.startswith("```"):
        code = code[3:]
    if code.endswith("```"):
        code = code[:-3]
    code = code.strip()

    if not validate_python_code(code):
        return None

    filename = f"{tool_name}.py"
    filepath = os.path.join(GENERATED_TOOLS_DIR, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)
        
    print(f"Successfully synthesized and validated new tool: {filepath}")
    return filepath

if __name__ == "__main__":
    # Test tool generation: SHA-256 Hash Tool
    synthesize_and_register_tool(
        tool_name="tool_sha256_hasher",
        task_description="Create a tool function `hash_sha256(text: str) -> str` that computes and returns the hex SHA-256 hash of an input string."
    )
