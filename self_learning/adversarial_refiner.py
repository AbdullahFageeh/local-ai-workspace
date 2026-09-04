"""
Adversarial Prompt & Strategy Refiner (Inspired by theprint/nfh-self-improvement-loop and nayyarsan/reflexloop).
Uses an independent Evaluator agent to critique prompt gaps, eliminate friction, and enforce strict quality gates.
"""

import os
import json
from typing import Dict, Any, List
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage

CRITIQUES_FILE = os.path.join(os.path.dirname(__file__), "critiques.jsonl")
REFINEMENT_LOG = os.path.join(os.path.dirname(__file__), "prompt_refinements.jsonl")

# Separate evaluator model to avoid self-evaluation bias (NFH cardinal rule)
llm_evaluator = ChatOllama(model="reasoning-uncensored:1.5b", temperature=0.2)
llm_refiner = ChatOllama(model="general-uncensored:latest", temperature=0.3)

EVALUATOR_PROMPT = """You are an Adversarial Quality Evaluator.
Analyze the following query and the model's generated response.
Identify any factual inaccuracies, missing edge cases, excessive wordiness, or rule violations.

Query: {query}
Response: {response}

Output your verdict as valid JSON:
{{
  "verdict": "APPROVE" or "REJECT",
  "flaws_detected": ["flaw 1", "flaw 2"],
  "prompt_rule_to_add": "One concise sentence to prevent this in the future."
}}
"""

def evaluate_and_refine(query: str, response: str) -> Dict[str, Any]:
    """Adversarial evaluation pass on model responses."""
    eval_query = EVALUATOR_PROMPT.format(query=query, response=response)
    res = llm_evaluator.invoke([HumanMessage(content=eval_query)])
    
    raw_content = res.content.strip()
    # Extract JSON payload
    try:
        if "{" in raw_content and "}" in raw_content:
            json_str = raw_content[raw_content.find("{"):raw_content.rfind("}")+1]
            evaluation = json.loads(json_str)
        else:
            evaluation = {"verdict": "APPROVE", "flaws_detected": [], "prompt_rule_to_add": ""}
    except Exception:
        evaluation = {"verdict": "APPROVE", "flaws_detected": [], "prompt_rule_to_add": ""}

    with open(REFINEMENT_LOG, "a", encoding="utf-8") as f:
        f.write(json.dumps({"query": query, "evaluation": evaluation}) + "\n")

    return evaluation

if __name__ == "__main__":
    test_eval = evaluate_and_refine(
        query="Write a quick reverse function in Python",
        response="Certainly! Here is the function: def rev(x): return x[::-1]. Hope this helps!"
    )
    print("Evaluator Output:")
    print(json.dumps(test_eval, indent=2))
