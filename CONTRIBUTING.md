# Contributing to Local AI Workspace

Thank you for your interest in contributing to the Local AI Workspace & LangGraph Multi-Model Router project!

---

## 🛠️ Development Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/AbdullahFageeh/local-ai-workspace.git
   cd local-ai-workspace
   ```

2. **Install Dependencies:**
   ```bash
   pip install langgraph langchain-ollama langchain-core fastapi uvicorn duckduckgo-search beautifulsoup4 sympy pillow
   ```

3. **Ensure Ollama Models are Installed:**
   ```bash
   ollama pull llama3.2:3b
   ollama pull qwen2.5-coder:3b
   ollama pull deepseek-r1:1.5b
   ollama pull moondream:latest
   ollama pull nomic-embed-text:latest
   ollama create coder-architect:latest -f Modelfile.coder_architect
   ```

---

## 🧪 Testing Guidelines

Before submitting a Pull Request, run the automated router test suite:

```bash
python test_router.py
```

Ensure all 5 routing categories (General, Quick Code, Complex Code, Reasoning, and Vision) pass without errors.

---

## 📋 Pull Request Process

1. Fork the repository and create your branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```
2. Commit your changes with clear, concise commit messages.
3. Push to your fork and submit a Pull Request to `main`.
4. Describe what changed and include test results in the PR description.
