"""
Demo: Autonomous Self-Learning & Self-Improving Loop in Action.
Walks through a live 4-step autonomous evolution cycle:
  1. Capture user prompt & execution trajectory.
  2. Detect missing capability and dynamically synthesize a new Python tool.
  3. Run adversarial quality evaluation using an isolated model.
  4. Sync approved output to the continuous training buffer for fine-tuning.
"""

import time
import os
import json
from self_learning.experience_logger import log_experience, log_critique
from self_learning.tool_generator import synthesize_and_register_tool
from self_learning.adversarial_refiner import evaluate_and_refine
from self_learning.continuous_learning_buffer import sync_experiences_to_training_buffer

def run_live_self_learning_demo():
    print("=" * 75)
    print("🤖 LIVE DEMO: AUTONOMOUS SELF-LEARNING AGENT FLYWHEEL")
    print("=" * 75)

    # Simulation Scenario: User asks for a custom Base64 URL-safe encoder tool
    user_query = "Create a fast URL-safe Base64 encoder function in Python."
    print(f"\n[Scenario]: User prompt received -> \"{user_query}\"")
    time.sleep(1)

    # Step 1: Trajectory & Experience Capture
    print("\n[Step 1/4] 📝 Logging Interaction Trajectory (Prax / Reflexloop)...")
    simulated_response = (
        "```python\nimport base64\n\ndef url_safe_b64encode(text: str) -> str:\n"
        "    return base64.urlsafe_b64encode(text.encode('utf-8')).decode('utf-8').rstrip('=')\n```"
    )
    exp = log_experience(
        query=user_query,
        response=simulated_response,
        model_used="coder-uncensored:7b",
        category="quick_code",
        success=True
    )
    print(f"-> Trajectory logged with timestamp: {exp['timestamp']}")
    time.sleep(1)

    # Step 2: Autonomous Tool Self-Synthesis
    print("\n[Step 2/4] 🛠️ Autonomous Tool Self-Synthesis (Miguel / Cogitator-AI)...")
    print("-> Agent detected reusable skill gap: 'tool_url_safe_base64'")
    tool_path = synthesize_and_register_tool(
        tool_name="tool_url_safe_base64",
        task_description="Create a Python function `encode_url_safe_b64(data: str) -> str` that performs URL-safe Base64 encoding without padding."
    )
    print(f"-> New Python tool synthesized & AST-verified at: {tool_path}")
    time.sleep(1)

    # Step 3: Adversarial Self-Critique & Evaluation
    print("\n[Step 3/4] ⚖️ Adversarial Critique & Evaluation (NFH Loop / Reflexloop)...")
    print("-> Triggering independent Evaluator (reasoning-uncensored:1.5b)...")
    eval_res = evaluate_and_refine(query=user_query, response=simulated_response)
    print(f"-> Evaluator Verdict: [{eval_res.get('verdict', 'APPROVE')}]")
    if eval_res.get("prompt_rule_to_add"):
        print(f"-> Suggested Prompt Refinement: \"{eval_res['prompt_rule_to_add']}\"")
    time.sleep(1)

    # Step 4: Continuous Fine-Tuning Flywheel Sync
    print("\n[Step 4/4] 🦥 Continuous Learning Buffer Sync (Soup / Unsloth)...")
    count = sync_experiences_to_training_buffer()
    print(f"-> Continuous fine-tuning buffer updated. Total verified dataset rows: {count}")

    print("\n" + "=" * 75)
    print("✅ SELF-LEARNING DEMO COMPLETE: The AI has evolved its tools & dataset.")
    print("=" * 75)

if __name__ == "__main__":
    run_live_self_learning_demo()
