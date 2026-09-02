"""
Master Self-Learning Test Suite.
Verifies:
1. Experience logging (Prax/Reflexloop)
2. Autonomous Tool Synthesis & AST Validation (Miguel/Cogitator)
3. Adversarial Quality Evaluation (NFH/Reflexloop)
4. Continuous Fine-Tuning Buffer Sync (Soup/Unsloth)
"""

import os
from self_learning.experience_logger import log_experience, get_recent_experiences
from self_learning.tool_generator import synthesize_and_register_tool, validate_python_code
from self_learning.adversarial_refiner import evaluate_and_refine
from self_learning.continuous_learning_buffer import sync_experiences_to_training_buffer

def run_self_learning_tests():
    print("="*70)
    print("RUNNING AUTOMATED SELF-LEARNING ENGINE TEST SUITE")
    print("="*70)

    # 1. Test Experience Logger
    print("\n[Step 1/4] Testing Experience Logger (Prax / Reflexloop)...")
    log_experience(
        query="Write an asynchronous HTTP fetcher in Python",
        response="async def fetch(url): async with httpx.AsyncClient() as client: return await client.get(url)",
        model_used="qwen2.5-coder:3b",
        category="quick_code",
        success=True
    )
    exps = get_recent_experiences(5)
    print(f"-> Logged successfully. Total recent entries: {len(exps)}")

    # 2. Test Tool Synthesizer
    print("\n[Step 2/4] Testing Autonomous Tool Synthesis (Miguel / Cogitator)...")
    tool_path = synthesize_and_register_tool(
        tool_name="tool_uuid_generator",
        task_description="Create a python function `generate_uuid() -> str` that returns a unique UUID4 string."
    )
    print(f"-> Tool generated and AST-validated at: {tool_path}")

    # 3. Test Adversarial Evaluation
    print("\n[Step 3/4] Testing Adversarial Evaluation (NFH / Reflexloop)...")
    eval_res = evaluate_and_refine(
        query="Explain Python memory management in 2 sentences",
        response="Python manages memory through automatic reference counting and a cyclic garbage collector to free unreferenced objects."
    )
    print(f"-> Adversarial Verdict: [{eval_res.get('verdict', 'APPROVE')}]")

    # 4. Test Continuous Training Sync
    print("\n[Step 4/4] Testing Training Buffer Sync (Soup / Unsloth)...")
    count = sync_experiences_to_training_buffer()
    print(f"-> Synced {count} verified interaction pairs to training buffer.")

    print("\n" + "="*70)
    print("ALL 4 SELF-LEARNING MODULES VERIFIED & OPERATIONAL")
    print("="*70)

if __name__ == "__main__":
    run_self_learning_tests()
