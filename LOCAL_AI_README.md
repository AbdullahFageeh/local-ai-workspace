# Local AI Workspace Setup & Usage Guide

A private, offline AI assistant environment running on your local machine using **Ollama** and **Open-WebUI**.

---

## 🖥️ System & Hardware

- **GPU:** NVIDIA GeForce GTX 1660 Ti (6 GB VRAM)
- **Environment:** Windows 11 / PowerShell 7+ / Python 3.12
- **Backend Engine:** Ollama (GPU-accelerated)
- **Frontend UI:** Open-WebUI (Web interface at `http://localhost:8080`)

---

## 🚀 Quick Start

### Option 1: Desktop Shortcut
Double-click the **`AI Workspace`** shortcut on your Desktop.

### Option 2: PowerShell
Run the startup script directly:
```powershell
.\Start-AIWorkspace.ps1
```

This will:
1. Ensure the Ollama backend service is running.
2. Automatically launch your default browser to `http://localhost:8080`.
3. Start the Open-WebUI server in your terminal.

---

## 📦 Installed Models

| Model | Size | VRAM Usage | Best For |
|---|---|---|---|
| **`coder-architect:latest`** | ~4.7 GB | ~4.7 GB | Custom persona: Staff Engineer with automatic threading locks & strict typing |
| **`deepseek-r1:1.5b`** | ~1.1 GB | ~1.5 GB | Deep step-by-step logic, math proofs, and deductive reasoning |
| **`moondream:latest`** | ~1.7 GB | ~2.0 GB | Multimodal Vision: Describe, analyze, and query images |
| **`llama3.2:3b`** | ~2.0 GB | ~2.0 GB | Daily assistant, summarization, general chat |
| **`qwen2.5-coder:3b`** | ~1.9 GB | ~2.2 GB | Fast coding, syntax queries, lightweight scripting |
| **`qwen2.5-coder:7b`** | ~4.7 GB | ~4.7 GB | Advanced programming, complex algorithms, multi-threading |
| **`nomic-embed-text:latest`** | ~274 MB | ~0.3 GB | High-speed document vector embedding for Open-WebUI RAG |

---

## ⚡ Performance & Reddit Optimizations Applied
- `OLLAMA_KEEP_ALIVE=1h`: Models stay hot in VRAM for instant follow-up answers without reload delays.
- `OLLAMA_NUM_PARALLEL=2`: Supports multiple simultaneous queries.
- `coder-architect`: Pre-built persona running at `temperature 0.2` and `num_ctx 8192` for reliable, bug-free coding.

---

## 🛠️ Custom Tools & Skills

The following custom tools have been created and packaged for Open-WebUI:

1. **Web Search Tool (`tools_web_search.py`):** Live DuckDuckGo search for current news and technical documentation.
2. **Calculator & Math Tool (`tools_calculator.py`):** SymPy formula, calculus, and high-precision evaluation.
3. **URL Reader & Scraper Tool (`tools_url_reader.py`):** Extracts clean text from public web links.
4. **Workspace Search Tool (`tools_workspace_search.py`):** Search code patterns and files across your local workspace.
5. **Code Validator Tool (`tools_code_validator.py`):** Validate Python syntax, check type hints, and count LOC.

### How to enable tools in Open-WebUI:
1. Start your workspace with `.\Start-AIWorkspace.ps1`.
2. In Open-WebUI (`http://localhost:8080`), navigate to **Workspace > Tools**.
3. Click **"+"** (Add Tool), and copy/paste the content from any `tools_*.py` file.
4. Click **Save**. The tools will be available to models that support function calling.

---

## 📚 Knowledge Base (RAG)

Knowledge base reference documents have been created in `ai_knowledge_base/`:
- **`python_engineering_guide.md`:** Data structure complexities, threading patterns, clean code rules.
- **`powershell_system_guide.md`:** Windows process management, network diagnostics, path handling.
- **`ai_hardware_profile.md`:** GPU architecture limits, VRAM budgets, local port references.
- **`copilot_coding_workflow.md`:** Root-cause debugging, narrow-edit discipline, validation-first workflow patterns.

### How to attach knowledge to all models:
1. In Open-WebUI (`http://localhost:8080`), go to **Workspace > Knowledge**.
2. Click **"+"** (Create Knowledge Collection) and name it (e.g., `Engineering Knowledge`).
3. Upload or drag-and-drop the files from `ai_knowledge_base/`.
4. In any chat, type `#Engineering Knowledge` to ground the model's answers with these documents.

---

## 🌐 LangGraph Multi-Model API Server

You can run the router as a background REST API server:
```powershell
python C:\Users\abdul\langgraph_api.py
```

### Endpoints
- **Interactive Swagger Docs:** `http://localhost:8001/docs`
- **Native Chat Route:** `POST http://localhost:8001/chat`
  ```json
  {"query": "Write a thread-safe cache in Python"}
  ```
- **OpenAI-Compatible Route:** `POST http://localhost:8001/v1/chat/completions`
  - Drop-in backend for VS Code (Continue/Cline), Cursor, or external applications.

---

## 💻 VS Code Extension Setup (Continue / Cline)

Configuration has been pre-written to `~/.continue/config.json`:
- **Main Chat Assistant:** `Local LangGraph Multi-Model Router` (`http://localhost:8001/v1`)
- **Direct Coding:** `coder-architect:latest` (Ollama `http://localhost:11434`)
- **Inline Tab-Autocomplete:** `qwen2.5-coder:3b`
- **Codebase Indexing (Embeddings):** `nomic-embed-text:latest`

### How to use in VS Code:
1. Install the **Continue** extension from the VS Code Marketplace.
2. Ensure either `ollama` or `python C:\Users\abdul\langgraph_api.py` is running.
3. Open the Continue sidebar in VS Code (`Ctrl+L`) to chat or highlight code and press `Ctrl+I` to edit inline.

---

## 💻 CLI Commands (Ollama)

You can also run models directly in your terminal without the web UI:

- **Interactive chat:**
  ```powershell
  ollama run llama3.2:3b
  ```
- **Single query:**
  ```powershell
  ollama run qwen2.5-coder:7b "Explain how Python GIL works in 2 sentences"
  ```
- **List installed models:**
  ```powershell
  ollama list
  ```
- **Pull a new model:**
  ```powershell
  ollama pull mistral:7b
  ```
- **Delete a model to free disk space:**
  ```powershell
  ollama rm <model-name>
  ```

---

## ⚙️ Maintenance & Troubleshooting

- **Server Exit Code 1 on Ctrl+C:** Normal behavior when stopping the server via keyboard interrupt in PowerShell.
- **Port Conflict:** If port `8080` is in use, start Open-WebUI on another port:
  ```powershell
  $env:PORT = "8085"; open-webui serve
  ```
