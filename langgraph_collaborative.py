"""
Multi-Agent Collaborative Refinement Graph with RAG and Tools.
Workflow:
1. RETRIEVAL: Search workspace and knowledge base for relevant context.
2. CODER: Generates a draft using the retrieved context.
3. CRITIC: Evaluates the draft for flaws, edge cases, and rule violations.
4. CODER: Refines the solution based on the critique.
"""

from typing import TypedDict, Optional
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, START, END
import os
import re

# --- State Definition ---
class CollaborativeState(TypedDict):
    query: str
    context: str  # Retrieved context from tools/RAG
    draft: str
    critique: str
    final_response: str
    model_used: str

# --- Model Clients ---
llm_coder = ChatOllama(model="coder-architect:latest", temperature=0.2)
llm_critic = ChatOllama(model="reasoning-uncensored:1.5b", temperature=0.4)

# --- Tools & RAG Functions ---

def search_workspace(query: str) -> str:
    """Search workspace files and knowledge base for relevant text."""
    results = []
    workspace = os.path.expanduser("~")  # Can be narrowed to a specific repo path
    keywords = [re.escape(word) for word in query.split()[:3] if word]
    pattern = "|".join(keywords)
    knowledge_base = os.path.join(os.path.dirname(__file__), "ai_knowledge_base")
    
    # 1. Search Knowledge Base
    if os.path.exists(knowledge_base):
        for fname in os.listdir(knowledge_base):
            if fname.endswith(".md"):
                with open(os.path.join(knowledge_base, fname), 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Simple keyword matching (case-insensitive)
                    if pattern and re.search(pattern, content, re.IGNORECASE):
                        results.append(f"[{fname}]\n{content[:500]}...")

    # 2. Search Python files in workspace
    for root, dirs, files in os.walk(workspace):
        # Skip hidden/large dirs
        if any(x in root for x in ['.git', 'node_modules', '__pycache__']):
            continue
        for f in files:
            if f.endswith(".py"):
                with open(os.path.join(root, f), 'r', encoding='utf-8', errors='ignore') as file:
                    content = file.read()
                    if re.search(query.split()[0:3], content, re.IGNORECASE):
                        results.append(f"[{f}]\n{content[:300]}...")
                        if len(results) >= 3: return "\n\n---\n\n".join(results)

    return "\n\n---\n\n".join(results) if results else "No relevant context found."


# --- Nodes ---

def retrieval_node(state: CollaborativeState) -> CollaborativeState:
    """Search for relevant context to aid the Coder."""
    # Take first few words as keywords for local search
    keywords = " ".join(state["query"].split()[:5])
    context = search_workspace(keywords)
    return {"context": context}

def draft_node(state: CollaborativeState) -> CollaborativeState:
    """Coder drafts an initial solution using context."""
    system = SystemMessage(content=f"""You are a Staff Software Engineer. 
Use the provided CONTEXT to answer the query. 
Write a robust, efficient solution with type hints. 
Focus on correctness, performance, and root-cause fixes.
DO NOT output JSON tool calls; write natural text and code blocks.""")
    
    prompt = f"""
Context from Workspace/Knowledge Base:
{state['context']}

User Query: {state['query']}
"""
    response = llm_coder.invoke([system, HumanMessage(content=prompt)])
    return {"draft": response.content}

def critique_node(state: CollaborativeState) -> CollaborativeState:
    """Critic evaluates the draft for flaws, edge cases, and rule violations."""
    system = SystemMessage(content="You are a Senior Architect Critic. Analyze the provided code draft. Identify logic errors, missing type hints, concurrency issues, or edge cases. Be concise and actionable.")
    response = llm_critic.invoke([
        system, 
        HumanMessage(content=f"Original Query: {state['query']}\n\nDraft Code:\n{state['draft']}")
    ])
    return {"critique": response.content}

def refine_node(state: CollaborativeState) -> CollaborativeState:
    """Coder refines the draft based on the critic's feedback."""
    system = SystemMessage(content="You are a Staff Software Engineer. Refine your previous draft to address all the critic's points. Ensure all fixes are applied correctly.")
    response = llm_coder.invoke([
        system,
        HumanMessage(content=f"Original Query: {state['query']}\n\nPrevious Draft:\n{state['draft']}\n\nCritique/Feedback:\n{state['critique']}")
    ])
    return {"final_response": response.content, "model_used": "coder-architect + reasoning-uncensored (Collaborative + RAG)"}

# --- Graph Construction ---
workflow = StateGraph(CollaborativeState)

workflow.add_node("retrieval", retrieval_node)
workflow.add_node("draft", draft_node)
workflow.add_node("critique", critique_node)
workflow.add_node("refine", refine_node)

workflow.add_edge(START, "retrieval")
workflow.add_edge("retrieval", "draft")
workflow.add_edge("draft", "critique")
workflow.add_edge("critique", "refine")
workflow.add_edge("refine", END)

app = workflow.compile()

# --- Execution Interface ---
def collaborate(query: str):
    initial_state = {"query": query, "context": "", "draft": "", "critique": "", "final_response": "", "model_used": ""}
    result = app.invoke(initial_state)
    print(f"[Context]: {result['context'][:100]}...")
    print(f"[Draft]: {result['draft'][:100]}...")
    print(f"[Critique]: {result['critique'][:100]}...")
    print(f"[Final Answer]:\n{result['final_response']}\n" + "-"*60)
    return result