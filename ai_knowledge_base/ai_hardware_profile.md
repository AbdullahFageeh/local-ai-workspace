# Local AI Operations, LLM Quantization & Hardware Guide

## Local Hardware Profile
- **Primary GPU:** NVIDIA GeForce GTX 1660 Ti (6 GB GDDR6 VRAM, Turing architecture).
- **Compute Capability & Limits:** Supports FP16 precision. Does not support native BF16 or FlashAttention-2.
- **VRAM Budgets:**
  - 3B parameter models (4-bit Q4_K_M): ~2.0 GB VRAM.
  - 7B parameter models (4-bit Q4_K_M): ~4.7 GB VRAM.
  - Models >13B: Exceeds 6 GB VRAM; requires CPU offloading or layer streaming.

## Core Services & Ports
- **Ollama Engine:** Runs on `http://localhost:11434` (OpenAI-compatible REST API).
- **Open-WebUI Frontend:** Runs on `http://localhost:8080` (Vector RAG, Tool integrations, user accounts).
