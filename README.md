## 🌟 Project Release & Summary

**GitHub Repository:** [https://github.com/AbdullahFageeh/local-ai-workspace](https://github.com/AbdullahFageeh/local-ai-workspace)  
**Latest Release:** [v1.0.0](https://github.com/AbdullahFageeh/local-ai-workspace/releases/tag/v1.0.0)

### Key Capabilities at a Glance:
- **Intelligent Intent-Based Routing:** Automatically classifies user prompts and routes them to the ideal model (General Chat, Quick Code, Concurrency Architecture, Logic Reasoning, or Vision).
- **100% Offline & Private:** Zero cloud API dependencies; runs fully GPU-accelerated on a consumer 6 GB GPU.
- **Unified Interfaces:** Connect via Browser (Open-WebUI), REST API (FastAPI), CLI Terminal, or IDE (VS Code Continue).
- **Extensible:** Pre-packaged with Web Search, Math Solver, and HTML Web Scraper tool plugins plus local RAG knowledge bases.

---

## 🖥️ System & Hardware Architecture

- **GPU:** NVIDIA GeForce GTX 1660 Ti (6 GB GDDR6 VRAM, Turing Architecture, FP16)
- **Host OS:** Windows 11 / PowerShell 7.6.5 / Python 3.12.10
- **Model Engine:** Ollama (GPU-accelerated, port `11434`)
- **Web UI:** Open-WebUI (Browser chat at `http://localhost:8080`)
- **API Server:** FastAPI + LangGraph StateGraph (Router API at `http://localhost:8000`)
- **IDE Plugin:** VS Code Continue extension configured via `~/.continue/config.json`

---

## 📦 Model Inventory & Modalities

| Model | Modality | Size | VRAM | Optimal Use Case |
|---|---|---|---|---|
| **`coder-architect:latest`** | Code / Concurrency | ~4.7 GB | ~4.7 GB | Staff Engineer persona: multi-threading locks, clean typing, systems architecture |
| **`deepseek-r1:1.5b`** | Reasoning | ~1.1 GB | ~1.5 GB | Step-by-step logic chains, math puzzles, deductive reasoning |
| **`moondream:latest`** | Multimodal Vision | ~1.7 GB | ~2.0 GB | Image captioning, visual inspection, screenshot QA |
| **`llama3.2:3b`** | General Chat & Router | ~2.0 GB | ~2.0 GB | Fast conversational replies, intent classification, summarization |
| **`qwen2.5-coder:3b`** | Fast Code | ~1.9 GB | ~2.2 GB | Rapid syntax lookup, one-liner scripts, autocomplete |
| **`nomic-embed-text:latest`** | Embeddings | ~274 MB | ~0.3 GB | High-speed document vector embedding for Open-WebUI RAG |

---

## 🚀 Quick Launch Options

### 1. Web Browser Interface (Open-WebUI)
- **Desktop Shortcut:** Double-click the **`AI Workspace`** shortcut on your Desktop.
- **PowerShell Script:**
  ```powershell
  .\Start-AIWorkspace.ps1
  ```
  *Opens browser to `http://localhost:8080` and starts the WebUI server.*

### 2. Multi-Model Router API Server (FastAPI + LangGraph)
Start the unified multi-model router endpoint:
```powershell
python C:\Users\abdul\langgraph_api.py
```
- **Interactive Swagger Docs:** `http://localhost:8000/docs`
- **Native Endpoint:** `POST http://localhost:8000/chat`
- **OpenAI-Compatible Endpoint:** `POST http://localhost:8000/v1/chat/completions`

### 3. Run Router Direct in Terminal
```powershell
python C:\Users\abdul\langgraph_router.py "Design a thread-safe connection pool in Python"
```

### 4. Run Automated Test Suite
```powershell
python C:\Users\abdul\test_router.py
```

---

## 🛠️ Custom Tools & Plugins

Created ready-to-use Python tool modules for Open-WebUI in your home folder:
- **`tools_web_search.py`:** Live DuckDuckGo web search.
- **`tools_calculator.py`:** SymPy math and formula evaluation.
- **`tools_url_reader.py`:** HTML web page scraper.

*To activate in Open-WebUI: Go to **Workspace > Tools > "+"**, paste the file content, and click **Save**.*

---

## 📚 Knowledge Base (RAG)

Pre-built documentation stored in `C:\Users\abdul\ai_knowledge_base\`:
- **`python_engineering_guide.md`:** Data structures, threading patterns, and complexity rules.
- **`powershell_system_guide.md`:** Windows administrative, process, and networking reference.
- **`ai_hardware_profile.md`:** Hardware capabilities, VRAM constraints, and local port maps.

*To activate in Open-WebUI: Go to **Workspace > Knowledge > "+"**, create a collection, and upload the markdown files.*

---

## 💻 VS Code Continue Extension Setup

Configuration file is pre-configured at `C:\Users\abdul\.continue\config.json`:
- **Chat Assistant (`Ctrl+L`):** `Local LangGraph Multi-Model Router` (`http://localhost:8000/v1`)
- **Direct Coding:** `coder-architect:latest` (`http://localhost:11434`)
- **Tab Autocomplete:** `qwen2.5-coder:3b`
- **Codebase Embeddings:** `nomic-embed-text:latest`

---

## ⚡ Performance Settings Applied

- `OLLAMA_KEEP_ALIVE=1h`: Models stay resident in GPU memory for instantaneous follow-up prompts.
- `OLLAMA_NUM_PARALLEL=2`: Concurrently handles dual model requests.
- `coder-architect`: Hardcoded with `temperature 0.2` and `num_ctx 8192` for reliable, bug-free code generation.
