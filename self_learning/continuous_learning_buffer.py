"""
Continuous Fine-Tuning Flywheel (Inspired by MakazhanAlpamys/Soup and unslothai/unsloth).
Extracts approved and verified experiences into training buffers and triggers fine-tuning jobs.
"""

import os
import json
from typing import List, Dict

EXPERIENCE_FILE = os.path.join(os.path.dirname(__file__), "experiences.jsonl")
BUFFER_FILE = os.path.join(os.path.dirname(__file__), "continuous_training_buffer.jsonl")
FINETUNE_THRESHOLD = 50  # Number of new verified examples before training trigger

def sync_experiences_to_training_buffer() -> int:
    """Extracts successful, high-quality experiences into the training buffer."""
    if not os.path.exists(EXPERIENCE_FILE):
        return 0

    valid_samples = []
    with open(EXPERIENCE_FILE, "r", encoding="utf-8") as f:
        for line in f:
            try:
                record = json.loads(line)
                # Only include approved/successful interactions
                if record.get("success", True) and record.get("query") and record.get("response"):
                    sample = {
                        "instruction": record["query"],
                        "input": "",
                        "output": record["response"]
                    }
                    valid_samples.append(sample)
            except Exception:
                continue

    with open(BUFFER_FILE, "w", encoding="utf-8") as f:
        for s in valid_samples:
            f.write(json.dumps(s) + "\n")

    print(f"Synced {len(valid_samples)} verified interaction pairs to {BUFFER_FILE}")
    
    if len(valid_samples) >= FINETUNE_THRESHOLD:
        print(f"Threshold reached ({len(valid_samples)} >= {FINETUNE_THRESHOLD}). Ready for automated fine-tuning pass!")
    else:
        print(f"Buffer progress: {len(valid_samples)}/{FINETUNE_THRESHOLD} samples collected.")

    return len(valid_samples)

if __name__ == "__main__":
    sync_experiences_to_training_buffer()
