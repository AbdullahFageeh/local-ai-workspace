"""
Test script to verify LangGraph router delegation across all 5 specialized nodes:
  1. General Chat (llama3.2:3b)
  2. Quick Code (qwen2.5-coder:3b)
  3. Complex Architecture (coder-architect:latest)
  4. Deep Reasoning (deepseek-r1:1.5b)
  5. Multimodal Vision (moondream:latest)
"""

import os
from PIL import Image, ImageDraw
from langgraph_router import app

def run_tests():
    print("="*70)
    print("STARTING LANGGRAPH MULTI-MODEL ROUTER TEST SUITE")
    print("="*70)

    # 1. Create a dummy test image for the vision test
    test_img_path = os.path.abspath("test_sample_image.png")
    img = Image.new("RGB", (200, 200), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    d.text((20, 90), "Local AI Test", fill=(255, 255, 0))
    img.save(test_img_path)

    test_cases = [
        {
            "name": "General Chat Test",
            "query": "What are 2 good habits for better sleep?",
            "image_path": None,
            "expected_category": "general"
        },
        {
            "name": "Quick Code Test",
            "query": "Write a Python one-liner to reverse a list.",
            "image_path": None,
            "expected_category": "quick_code"
        },
        {
            "name": "Complex Architecture Test",
            "query": "Design a thread-safe Singleton pattern in Python using threading.Lock with double-checked locking.",
            "image_path": None,
            "expected_category": "complex_code"
        },
        {
            "name": "Deep Reasoning Test",
            "query": "Solve this math logic puzzle: If 3 cats catch 3 mice in 3 minutes, how many cats are needed to catch 100 mice in 100 minutes? Prove step by step.",
            "image_path": None,
            "expected_category": "reasoning"
        },
        {
            "name": "Vision / Multimodal Test",
            "query": "Describe what you see in this image.",
            "image_path": test_img_path,
            "expected_category": "vision"
        }
    ]

    for idx, test in enumerate(test_cases, 1):
        print(f"\n[Test {idx}/5] {test['name']}")
        print(f"Query: \"{test['query']}\"")
        if test['image_path']:
            print(f"Image attached: {test['image_path']}")

        state = {
            "query": test["query"],
            "image_path": test["image_path"],
            "category": "general",
            "response": "",
            "model_used": ""
        }
        
        result = app.invoke(state)
        print(f"-> Categorized As: [{result['category']}] (Expected: [{test['expected_category']}])")
        print(f"-> Handled By: {result['model_used']}")
        print(f"-> Sample Response Snippet: {result['response'][:150]}...")
        print("-" * 50)

    # Cleanup test image
    if os.path.exists(test_img_path):
        os.remove(test_img_path)

    print("\nALL ROUTING TESTS COMPLETED.")

if __name__ == "__main__":
    run_tests()
