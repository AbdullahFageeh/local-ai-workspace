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

## 🖥️ System & Hardware Architecture

- **GPU:** NVIDIA GeForce GTX 1660 Ti (6 GB GDDR6 VRAM, Turing Architecture, FP16)
- **Host OS:** Windows 11 / PowerShell 7.6.5 / Python 3.12.10
- **Model Engine:** Ollama (GPU-accelerated, port `11434`)
- **Web UI:** Open-WebUI (Browser chat at `http://localhost:8080`)
- **API Server:** FastAPI + LangGraph StateGraph (Router API at `http://localhost:8000`)
- **IDE Plugin:** VS Code Continue extension configured via `~/.continue/config.json`

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
- **Interactive Swagger Docs:** `http://localhost:8000/docs`
- **Native Chat Route:** `POST http://localhost:8000/chat`
- **OpenAI-Compatible Route:** `POST http://localhost:8000/v1/chat/completions`

---

## 🧪 Running Automated Tests

Run the model routing test suite:
```powershell
python test_router.py
```

Run the autonomous self-learning test suite:
```powershell
python test_self_learning.py
```

---

## 📦 Project Structure

```text
local-ai-workspace/
├── Start-AIWorkspace.ps1        # 1-click startup script for Ollama & Open-WebUI
├── langgraph_router.py          # LangGraph StateGraph multi-model router
├── langgraph_api.py             # FastAPI server (native + OpenAI endpoints)
├── test_router.py               # Model routing test suite (5 modalities)
├── test_self_learning.py        # Master self-learning validation runner
├── Modelfile.coder_architect    # Custom Staff Engineer persona definition
├── tools_web_search.py          # Open-WebUI DuckDuckGo search tool
├── tools_calculator.py          # Open-WebUI SymPy math solver tool
├── tools_url_reader.py          # Open-WebUI web scraper tool
├── ai_knowledge_base/           # Markdown RAG documents for dev & system ops
├── finetuning/                  # Fine-tuning pipeline (Soup, Unsloth, LLaMA-Factory)
│   ├── dataset_builder.py       # Converts Q&A into Alpaca & JSONL formats
│   ├── soup.yaml                # Layer-streaming config for local 6GB GPU
│   ├── Unsloth_Finetune_Colab.ipynb # 1-click Google Colab notebook
│   ├── Start-LlamaFactory.ps1   # Visual browser fine-tuning dashboard
│   └── Export-ToOllama.ps1      # Imports GGUF weights into Ollama
├── self_learning/               # Autonomous self-improving engine
│   ├── experience_logger.py     # Trajectory & correction logger
│   ├── tool_generator.py        # Autonomous tool synthesis & AST validation
│   ├── adversarial_refiner.py   # Independent evaluator & prompt refiner
│   └── continuous_learning_buffer.py # Training buffer synchronization
├── README.md                    # Project overview & quick start guide
├── SELF_LEARNING_GUIDE.md       # Self-learning architecture deep dive
├── CONTRIBUTING.md              # Contributor guidelines & setup
└── LICENSE                      # MIT License
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
