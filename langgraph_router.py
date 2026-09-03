"""
LangGraph Multi-Model Router for Local Ollama Models.
Routes user queries between:
  - llama3.2:3b (General writing, questions, and router)
  - qwen2.5-coder:3b (Quick syntax and short scripts)
  - coder-architect:latest (Complex algorithms, systems design, multi-threading)
  - deepseek-r1:1.5b (Deep step-by-step logic and mathematical reasoning)
  - moondream:latest (Vision and image analysis)
"""

from typing import TypedDict, Literal, Optional
import sys
import json
import os
import time
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END

# Define Router State
class AgentState(TypedDict):
    query: str
    image_path: Optional[str]
    category: Literal["general", "quick_code", "complex_code", "reasoning", "vision"]
    response: str
    model_used: str
    history: list  # prior conversation turns for context

# Initialize Model Clients
llm_router = ChatOllama(model="llama3.2:3b", temperature=0.0)
llm_general = ChatOllama(model="llama3.2:3b", temperature=0.7)
llm_quick_code = ChatOllama(model="qwen2.5-coder:3b", temperature=0.2)
llm_architect = ChatOllama(model="coder-architect:latest", temperature=0.2)
llm_reasoning = ChatOllama(model="deepseek-r1:1.5b", temperature=0.6)
llm_vision = ChatOllama(model="moondream:latest")

CAVEMAN_SYSTEM_PROMPT = """[Concise Mode / Caveman Rules Active]:
1. Why use many words when few words do trick.
2. NO throat-clearing, pleasantries, filler, or preamble (never say "Sure, here is...", "Certainly!").
3. Give direct diagnosis, exact code, commands, and concrete answer immediately.
4. Keep all code blocks, syntax, type hints, and paths 100% exact and complete.
5. NEVER output raw JSON function calls or tool invocations — respond in natural language only."""

# Per-model system prompts — leverage the full capabilities of each model
SYSTEM_GENERAL = f"""{CAVEMAN_SYSTEM_PROMPT}

You are a versatile assistant. Answer questions, write text, explain concepts, and help with non-technical tasks. Be accurate and concise."""

SYSTEM_QUICK_CODE = f"""{CAVEMAN_SYSTEM_PROMPT}

You are a fast Python coder. Write clean, working code with type hints. Keep functions focused and self-contained. Include brief inline comments for non-obvious logic."""

SYSTEM_ARCHITECT = f"""{CAVEMAN_SYSTEM_PROMPT}

You are a Staff Software Engineer & Systems Architect.
- Fix problems at root cause, not symptoms.
- Make the smallest possible edit; preserve existing style and patterns.
- Use explicit type hints, threading.Lock where needed, and O(N) complexity notes.
- After proposing a fix, state how to verify it (test, command, or check).
- When a question is ambiguous, ask one clarifying question before exploring broadly."""

SYSTEM_REASONING = f"""{CAVEMAN_SYSTEM_PROMPT}

You are a deep reasoning engine. Work through logic step by step.
- State your assumptions explicitly.
- Show intermediate deductions, then conclude.
- Double-check arithmetic and logical consistency before final answer."""

# Experience logging integration
EXPERIENCE_FILE = os.path.join(os.path.dirname(__file__), "self_learning", "experiences.jsonl")

def _log_experience(query: str, response: str, model_used: str, category: str, success: bool = True):
    """Log interaction to self-learning buffer."""
    try:
        record = {
            "timestamp": time.time(),
            "query": query,
            "response": response,
            "model_used": model_used,
            "category": category,
            "success": success
        }
        os.makedirs(os.path.dirname(EXPERIENCE_FILE), exist_ok=True)
        with open(EXPERIENCE_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except Exception:
        pass  # Silent fail — don't break the conversation


# 1. Router Node: Classify user intent
def route_query(state: AgentState) -> AgentState:
    if state.get("image_path"):
        return {"category": "vision"}

    prompt = f"""You are an intent classifier. Categorize the user query into exactly one category:
- "general": everyday conversation, facts, writing, summaries, or non-technical questions.
- "quick_code": short code snippets, simple functions, syntax lookup, or one-liner scripts.
- "complex_code": multi-threading, concurrency, data structures, algorithms, system architecture, or full application design.
- "reasoning": logic puzzles, math proofs, step-by-step deductions, riddles, or complex word problems.

Respond ONLY with one word: general, quick_code, complex_code, or reasoning.

Query: {state['query']}
Category:"""
    res = llm_router.invoke([HumanMessage(content=prompt)])
    cat_raw = res.content.strip().lower()

    if "reason" in cat_raw or "math" in cat_raw or "puzzle" in cat_raw or "logic" in cat_raw:
        category = "reasoning"
    elif "complex" in cat_raw:
        category = "complex_code"
    elif "code" in cat_raw or "quick" in cat_raw:
        category = "quick_code"
    else:
        category = "general"

    return {"category": category}


# 2. Worker Nodes with per-model prompts and history context
def general_worker(state: AgentState) -> AgentState:
    messages = [{"role": "system", "content": SYSTEM_GENERAL}]
    # Add conversation history for context
    if state.get("history"):
        messages.extend(state["history"])
    messages.append({"role": "user", "content": state["query"]})
    res = llm_general.invoke(messages)
    response = res.content
    _log_experience(state["query"], response, "llama3.2:3b", "general")
    return {"response": response, "model_used": "llama3.2:3b (General - Caveman)"}

def quick_code_worker(state: AgentState) -> AgentState:
    messages = [{"role": "system", "content": SYSTEM_QUICK_CODE}]
    if state.get("history"):
        messages.extend(state["history"])
    messages.append({"role": "user", "content": state["query"]})
    res = llm_quick_code.invoke(messages)
    response = res.content
    _log_experience(state["query"], response, "qwen2.5-coder:3b", "quick_code")
    return {"response": response, "model_used": "qwen2.5-coder:3b (Quick Code - Caveman)"}

def architect_worker(state: AgentState) -> AgentState:
    messages = [{"role": "system", "content": SYSTEM_ARCHITECT}]
    if state.get("history"):
        messages.extend(state["history"])
    messages.append({"role": "user", "content": state["query"]})
    res = llm_architect.invoke(messages)
    response = res.content
    _log_experience(state["query"], response, "coder-architect:latest", "complex_code")
    return {"response": response, "model_used": "coder-architect:latest (Staff Architect - Caveman)"}

def reasoning_worker(state: AgentState) -> AgentState:
    messages = [{"role": "system", "content": SYSTEM_REASONING}]
    if state.get("history"):
        messages.extend(state["history"])
    messages.append({"role": "user", "content": state["query"]})
    res = llm_reasoning.invoke(messages)
    response = res.content
    _log_experience(state["query"], response, "deepseek-r1:1.5b", "reasoning")
    return {"response": response, "model_used": "deepseek-r1:1.5b (Deep Reasoning - Caveman)"}

def vision_worker(state: AgentState) -> AgentState:
    content = [{"type": "text", "text": f"{CAVEMAN_SYSTEM_PROMPT}\n\n{state['query']}"}]
    if state.get("image_path"):
        content.append({"type": "image_url", "image_url": state["image_path"]})
    res = llm_vision.invoke([HumanMessage(content=content)])
    return {"response": res.content, "model_used": "moondream:latest (Vision - Caveman)"}

# 3. Conditional Routing Decision
def decide_route(state: AgentState) -> str:
    return state["category"]

# 4. Build LangGraph
workflow = StateGraph(AgentState)

workflow.add_node("router", route_query)
workflow.add_node("general", general_worker)
workflow.add_node("quick_code", quick_code_worker)
workflow.add_node("complex_code", architect_worker)
workflow.add_node("reasoning", reasoning_worker)
workflow.add_node("vision", vision_worker)

workflow.add_edge(START, "router")
workflow.add_conditional_edges(
    "router",
    decide_route,
    {
        "general": "general",
        "quick_code": "quick_code",
        "complex_code": "complex_code",
        "reasoning": "reasoning",
        "vision": "vision"
    }
)
workflow.add_edge("general", END)
workflow.add_edge("quick_code", END)
workflow.add_edge("complex_code", END)
workflow.add_edge("reasoning", END)
workflow.add_edge("vision", END)

app = workflow.compile()

# 5. Execution Interface
def ask(query: str, image_path: Optional[str] = None):
    print(f"\n[Query]: {query}")
    initial_state = {"query": query, "image_path": image_path, "category": "general", "response": "", "model_used": ""}
    result = app.invoke(initial_state)
    print(f"[Routed To]: {result['model_used']}")
    print(f"[Answer]:\n{result['response']}\n" + "-"*60)
    return result

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_query = " ".join(sys.argv[1:])
        ask(user_query)
    else:
        print("Testing LangGraph with Reasoning and Logic Queries:")
        ask("If 5 machines take 5 minutes to make 5 widgets, how long would 100 machines take to make 100 widgets? Explain step by step.")
