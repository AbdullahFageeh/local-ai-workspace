# 🚀 Local AI Workspace & Autonomous Multi-Model Ecosystem

A 100% offline, private, GPU-accelerated local AI ecosystem running on consumer hardware (GTX 1660 Ti 6GB). Features multi-model dynamic routing with **LangGraph**, OpenAI-compatible **FastAPI** backend, **Open-WebUI** browser interface, **VS Code Continue** integration, a **3-framework fine-tuning pipeline**, and an **autonomous self-learning flywheel**.

---

## 🌟 Quick Overview & Capabilities

- **Intelligent Intent-Based Routing:** Uses LangGraph to automatically classify queries and route them to specialized local models:
  - **General Chat / Writing:** `llama3.2:3b`
  - **Quick Coding & Syntax:** `qwen2.5-coder:3b`
  - **Systems & Concurrency Architecture:** `coder-architect:latest` (7B)
  - **Deep Step-by-Step Reasoning & Math:** `deepseek-r1:1.5b`
  - **Multimodal Image Vision:** `moondream:latest`
  - **Vector Semantic Embeddings:** `nomic-embed-text:latest`
- **Caveman Prompt Optimization:** Squeezes out conversational filler ("Sure, here is..."), providing direct code and answers 3–4x faster with minimal token overhead.
- **Autonomous Self-Learning Flywheel (`self_learning/`):**
  - Logs user trajectories and corrections (`experience_logger.py`).
  - Synthesizes and AST-validates new Python tools at runtime (`tool_generator.py`).
  - Adversarially critiques answers using an isolated model (`adversarial_refiner.py`).
  - Aggregates verified data for continuous fine-tuning (`continuous_learning_buffer.py`).
- **Unified Interfaces:** Connect via Desktop Shortcut, Web Browser (Open-WebUI), REST API (FastAPI), CLI Terminal, or IDE (VS Code Continue).
- **Multi-Framework Fine-Tuning Pipeline (`finetuning/`):** Built-in support for **Soup** (1-command local layer streaming), **Unsloth** (1-click free Google Colab), and **LLaMA-Factory** (visual browser UI).

---

## 📚 Key Documentation & Guides

| Document | Description |
|---|---|
| **[`README.md`](README.md)** | High-level overview, architecture, and 3-step getting started guide. |
| **[`SELF_LEARNING_GUIDE.md`](SELF_LEARNING_GUIDE.md)** | Deep-dive architecture guide for the 4-pillar autonomous self-learning engine. |
| **[`LOCAL_AI_README.md`](LOCAL_AI_README.md)** | Hardware profile, port maps, VRAM budgets, and Open-WebUI setup tips. |
| **[`ROADMAP.md`](ROADMAP.md)** | Strategic future roadmap (MCP servers, multi-agent critic pairs, and voice agents). |
| **[`TEST_REPORT.md`](TEST_REPORT.md)** | Automated test execution logs confirming 100% test pass rates across all 5 modalities. |
| **[`CONTRIBUTING.md`](CONTRIBUTING.md)** | Development environment setup and pull request guidelines. |
| **[`LICENSE`](LICENSE)** | MIT Open-Source License. |

---

## 📦 Releases & Version Assets

- **[Release v2.1.0 (Latest)](https://github.com/AbdullahFageeh/local-ai-workspace/releases/tag/v2.1.0):** Live self-learning interactive demo and architecture deep-dive guide.
- **[Release v2.0.0](https://github.com/AbdullahFageeh/local-ai-workspace/releases/tag/v2.0.0):** Major release introducing the 4-pillar autonomous self-learning flywheel.
- **[Release v1.2.0](https://github.com/AbdullahFageeh/local-ai-workspace/releases/tag/v1.2.0):** Multi-framework fine-tuning pipeline (Soup, Unsloth, LLaMA-Factory).
- **[Release v1.1.0](https://github.com/AbdullahFageeh/local-ai-workspace/releases/tag/v1.1.0):** Caveman prompt optimization and 5-modality automated test suite.
- **[Release v1.0.0](https://github.com/AbdullahFageeh/local-ai-workspace/releases/tag/v1.0.0):** Initial core release with Ollama, Open-WebUI, LangGraph router, and FastAPI.

---

## 🚀 Getting Started in 3 Steps

### Step 1: Install & Launch Models
Ensure Ollama is running and download the core model suite:
```powershell
ollama pull llama3.2:3b
ollama pull qwen2.5-coder:3b
ollama pull deepseek-r1:1.5b
ollama pull moondream:latest
ollama pull nomic-embed-text:latest
ollama create coder-architect:latest -f Modelfile.coder_architect
```

### Step 2: Start the Web Workspace (Open-WebUI)
Double-click the **`AI Workspace`** desktop shortcut, or run:
```powershell
.\Start-AIWorkspace.ps1
```
*Opens your browser to `http://localhost:8080` with pre-configured tools (Web Search, SymPy Calculator, URL Scraper) and RAG knowledge bases.*

### Step 3: Run the Multi-Model Router API (For VS Code / Apps)
Start the background FastAPI router:
```powershell
python langgraph_api.py
```
- **Interactive Swagger Docs:** `http://localhost:8001/docs`
- **Native Chat Route:** `POST http://localhost:8001/chat`
- **OpenAI-Compatible Route:** `POST http://localhost:8001/v1/chat/completions`

---

## 🧪 Interactive Demos & Test Commands

- **Run Live Self-Learning Demo:**
  ```powershell
  python demo_self_learning.py
  ```
- **Run Routing Verification Test Suite:**
  ```powershell
  python test_router.py
  ```
- **Run Self-Learning Engine Tests:**
  ```powershell
  python test_self_learning.py
  ```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
