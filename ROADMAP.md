# 🗺️ Project Roadmap & Future Enhancements

This document outlines the strategic roadmap, planned milestones, and architectural goals for **Local AI Workspace**.

---

## 📍 Current Status: v2.1.0 (Production Ready)
- ✅ GPU-accelerated local model suite on 6 GB VRAM (`llama3.2:3b`, `qwen2.5-coder:3b`, `coder-architect:7b`, `deepseek-r1:1.5b`, `moondream`, `nomic-embed-text`).
- ✅ 1-click Desktop launcher and Open-WebUI with web search, calculator, scraper, and local RAG.
- ✅ LangGraph Multi-Model StateGraph router with Caveman prompt optimization.
- ✅ FastAPI server with native and OpenAI-compatible endpoints (`/v1/chat/completions`) for VS Code Continue.
- ✅ Multi-framework fine-tuning pipeline supporting **Soup**, **Unsloth**, and **LLaMA-Factory**.
- ✅ Autonomous 4-pillar self-learning flywheel with AST-validated tool synthesis and adversarial critique.

---

## 🎯 Phase 3: Autonomous Agent Extensions & MCP Integration (Q3 2026)

### 1. Model Context Protocol (MCP) Server Integration
- Embed an in-process MCP server into the LangGraph router.
- Allow local models to execute safe filesystem operations, terminal commands, and database queries across external applications.

### 2. Multi-Agent Collaborative Refinement (Coder + Critic Pair)
- Implement an automated dual-pass coding node:
  - `qwen2.5-coder:3b` generates candidate code.
  - `coder-architect:latest` (7B) automatically inspects the code for concurrency issues, edge cases, and type safety before returning the final response.

### 3. Persistent LangGraph Checkpoint Store
- Add SQLite-backed persistent memory to save full multi-turn conversation states across restarts without losing context.

---

## 🎯 Phase 4: Automated Continuous Fine-Tuning Daemon (Q4 2026)

### 1. Zero-Touch Nightly Training Scheduler
- Create a background worker that triggers local `soup train` runs whenever 50+ new verified interactions are logged in `continuous_training_buffer.jsonl`.
- Automatically benchmark new weights against baseline test suites before hot-swapping the model in Ollama.

### 2. Automated RAG Web Watcher
- Background crawler that watches technical documentation (e.g. Python, LangChain, PyTorch docs), generates fresh vector embeddings via `nomic-embed-text`, and automatically updates the local RAG store.

---

## 🎯 Phase 5: Voice & Edge Hardware Multi-Node Scaling (2027)

### 1. Local Voice-to-Voice (Whisper + Kokoro TTS)
- Integrate lightweight local speech recognition (`whisper.cpp`) and fast speech synthesis (`Kokoro-82M`) for real-time voice conversations with zero latency.

### 2. LAN Distributed Multi-Node Worker Pooling
- Distribute model execution across multiple local machines on the local area network (e.g., Laptop handles Vision/Router, Desktop handles 7B Coder).
