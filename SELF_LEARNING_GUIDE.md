# Autonomous Self-Learning & Self-Improving Architecture Guide

This document outlines the design, dataflow, and mechanics of the autonomous self-learning flywheel implemented in **Local AI Workspace**.

---

## 🏗️ Architecture Overview

The self-learning architecture is inspired by state-of-the-art open-source agent research:
- **`Bootstrappable/prax-agent` & `nayyarsan/reflexloop`:** Experience logging, trajectory tracking, and critique generation.
- **`soulfir/miguel` & `cogitator-ai/self-modifying`:** Autonomous tool synthesis, AST validation, and hot-loading.
- **`theprint/nfh-self-improvement-loop`:** Adversarial separation between generator and evaluator agents.
- **`MakazhanAlpamys/Soup` & `unslothai/unsloth`:** Continuous training dataset accumulation and QLoRA fine-tuning.

```
┌────────────────────────────────────────────────────────────────────────┐
│  1. CAPTURE              2. CRITIQUE              3. SYNTHESIZE        │
│  Daily Prompts & Errors ──► Adversarial Evaluator ──► Auto-Write Tools  │
│                                                          │             │
│  4. CONTINUOUS FINE-TUNE                                 ▼             │
│  Nightly Soup/Unsloth ◄──────────────────────── Auto-Sync Buffer       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 📦 Core Components & Files

### 1. Experience & Critique Logger (`self_learning/experience_logger.py`)
- **Purpose:** Records user queries, model responses, tool usage, latency, and explicit user corrections.
- **Artifacts:**
  - `self_learning/experiences.jsonl`: Interaction history and success flags.
  - `self_learning/critiques.jsonl`: Analytical critiques of flawed outputs.

### 2. Autonomous Tool Synthesizer (`self_learning/tool_generator.py`)
- **Purpose:** When a model identifies a missing skill or tool, this module writes a self-contained Python tool.
- **Safety Gate:** Uses Python's Abstract Syntax Tree (`ast.parse`) to validate syntax before saving to `self_learning/generated_tools/`.
- **Pre-generated Examples:**
  - `tool_sha256_hasher.py`: Computes SHA-256 hashes.
  - `tool_uuid_generator.py`: Generates RFC-compliant UUID4 strings.

### 3. Adversarial Prompt & Quality Refiner (`self_learning/adversarial_refiner.py`)
- **Purpose:** Evaluates answers against strict quality standards without self-grading bias.
- **Model Separation:** Uses an independent reasoning model (`deepseek-r1:1.5b`) to critique outputs produced by coder or general models.
- **Artifacts:** `self_learning/prompt_refinements.jsonl`.

### 4. Continuous Fine-Tuning Flywheel (`self_learning/continuous_learning_buffer.py`)
- **Purpose:** Filters approved, high-confidence interactions into an Alpaca-formatted dataset buffer (`continuous_training_buffer.jsonl`).
- **Trigger:** When the buffer reaches the threshold (e.g., 50 samples), it triggers a background training run using `finetuning/soup.yaml` or Google Colab Unsloth.

---

## 🧪 Verification & Testing

To run the complete self-learning verification suite:

```powershell
python C:\Users\abdul\local-ai-workspace\test_self_learning.py
```
