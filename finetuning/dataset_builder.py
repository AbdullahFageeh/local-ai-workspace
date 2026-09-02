"""
Dataset Builder for LLM Fine-Tuning.
Formats raw Q&A, instruction pairs, and conversation notes into:
1. Alpaca format (for Soup, Unsloth, LLaMA-Factory)
2. ShareGPT format (for Multi-turn conversation training)
"""

import json
import os
from typing import List, Dict

RAW_EXAMPLES = [
    {
        "instruction": "Write a thread-safe connection pool in Python with a maximum of 5 connections.",
        "input": "",
        "output": "```python\nimport threading\nfrom queue import Queue, Empty\n\nclass ConnectionPool:\n    def __init__(self, max_connections: int = 5):\n        self.max_connections = max_connections\n        self.pool = Queue(maxsize=max_connections)\n        self.lock = threading.Lock()\n        for i in range(max_connections):\n            self.pool.put(f'Connection-{i+1}')\n\n    def get_connection(self, timeout: float = 2.0):\n        try:\n            return self.pool.get(timeout=timeout)\n        except Empty:\n            raise TimeoutError('No connection available')\n\n    def release_connection(self, conn):\n        self.pool.put(conn)\n```"
    },
    {
        "instruction": "Explain how Python GIL impacts CPU-bound vs IO-bound multi-threading.",
        "input": "",
        "output": "The Python Global Interpreter Lock (GIL) allows only one native thread to execute Python bytecode at a time.\n- **CPU-bound tasks:** Multi-threading does not improve performance; use `multiprocessing` to bypass the GIL.\n- **IO-bound tasks:** Multi-threading works well because the GIL is released during network, disk, or sleep operations."
    },
    {
        "instruction": "Convert a given string to snake_case.",
        "input": "UserAccountSettings",
        "output": "```python\nimport re\n\ndef to_snake_case(name: str) -> str:\n    s1 = re.sub('(.)([A-Z][a-z]+)', r'\\1_\\2', name)\n    return re.sub('([a-z0-9])([A-Z])', r'\\1_\\2', s1).lower()\n```"
    }
]

def build_alpaca_dataset(data: List[Dict], output_path: str):
    """Save in standard Alpaca JSON format."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"Saved Alpaca dataset ({len(data)} rows) -> {output_path}")

def build_jsonl_dataset(data: List[Dict], output_path: str):
    """Save in JSONL format for Soup & Unsloth."""
    with open(output_path, "w", encoding="utf-8") as f:
        for row in data:
            f.write(json.dumps(row) + "\n")
    print(f"Saved JSONL dataset ({len(data)} rows) -> {output_path}")

if __name__ == "__main__":
    out_dir = os.path.dirname(os.path.abspath(__file__))
    build_alpaca_dataset(RAW_EXAMPLES, os.path.join(out_dir, "dataset_alpaca.json"))
    build_jsonl_dataset(RAW_EXAMPLES, os.path.join(out_dir, "dataset_training.jsonl"))
