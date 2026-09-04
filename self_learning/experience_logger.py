"""
Experience & Critique Logger (Inspired by Bootstrappable/prax-agent and nayyarsan/reflexloop).
Logs queries, model responses, tool usage, errors, user corrections, and autonomous critiques.
"""

import json
import os
import time
from typing import Dict, Any, Optional

EXPERIENCE_FILE = os.path.join(os.path.dirname(__file__), "experiences.jsonl")
CRITIQUE_FILE = os.path.join(os.path.dirname(__file__), "critiques.jsonl")

def log_experience(
    query: str,
    response: str,
    model_used: str,
    category: str,
    success: bool = True,
    correction: Optional[str] = None
) -> Dict[str, Any]:
    """Records interaction trajectory for continuous learning."""
    record = {
        "timestamp": time.time(),
        "query": query,
        "response": response,
        "model_used": model_used,
        "category": category,
        "success": success,
        "correction": correction
    }
    with open(EXPERIENCE_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")
    return record

def log_critique(
    session_id: str,
    weakness_identified: str,
    recommended_fix: str,
    gap_type: str  # e.g., "missing_tool", "prompt_gap", "logic_error"
) -> Dict[str, Any]:
    """Records analytical critique of a failed or sub-optimal output."""
    critique = {
        "timestamp": time.time(),
        "session_id": session_id,
        "weakness": weakness_identified,
        "recommended_fix": recommended_fix,
        "gap_type": gap_type
    }
    with open(CRITIQUE_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(critique) + "\n")
    return critique

def get_recent_experiences(limit: int = 20):
    if not os.path.exists(EXPERIENCE_FILE):
        return []
    with open(EXPERIENCE_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return [json.loads(line) for line in lines[-limit:]]

if __name__ == "__main__":
    # Test logger
    log_experience(
        query="Write a quick reverse function",
        response="def rev(s): return s[::-1]",
        model_used="coder-uncensored:7b",
        category="quick_code",
        success=True
    )
    print("Experience logger initialized and tested.")
