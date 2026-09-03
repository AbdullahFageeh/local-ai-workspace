"""
FastAPI Server exposing the LangGraph Multi-Model Router.
Endpoints: POST /chat, POST /v1/chat/completions, and POST /v1/completions
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import json
import time
import os
import uvicorn
from fastapi import Header
from langgraph_router import app as router_graph
from langgraph_collaborative import app as collaborative_graph

# Load .env file if it exists (requires python-dotenv)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = FastAPI(
    title="LangGraph Local Multi-Model API",
    description="Unified API routing queries between General, Quick Code, Architecture, Reasoning, and Vision local models.",
    version="1.0.0"
)

# API Key for unified access (loaded from .env, falls back to default if missing)
API_KEY = os.getenv("API_KEY", "sk-FCFF1BFC5225459373715577331AC09E996680279CE35523F21A3BBD2B6E42E0")

def verify_api_key(authorization: str = Header(None, alias="Authorization")):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = authorization.split(" ", 1)[1]
    if token != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API key")
    return token

class ChatRequest(BaseModel):
    query: str
    image_path: Optional[str] = None
    history: Optional[List[Dict[str, str]]] = None  # prior conversation turns

class ChatResponse(BaseModel):
    category: str
    model_used: str
    response: str

class OpenAIMessage(BaseModel):
    role: Optional[str] = "user"
    content: Any = ""

class OpenAIChatRequest(BaseModel):
    model: Optional[str] = "langgraph-router"
    messages: Optional[List[OpenAIMessage]] = []
    prompt: Optional[str] = None
    temperature: Optional[float] = 0.7
    stream: Optional[bool] = False


def _run_router(query: str, image_path: Optional[str] = None, history: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
    initial_state = {
        "query": query,
        "image_path": image_path,
        "history": history or [],
        "category": "general",
        "response": "",
        "model_used": ""
    }
    return router_graph.invoke(initial_state)


def _extract_prompt(prompt: Any) -> str:
    if isinstance(prompt, str) and prompt.strip():
        return prompt
    if isinstance(prompt, list):
        for item in reversed(prompt):
            if isinstance(item, str) and item.strip():
                return item
    return "Please complete or analyze the selected code."

def _extract_last_user_message(messages: Optional[List[OpenAIMessage]]) -> str:
    """Return text from the newest user message, never a tool result or assistant reply."""
    if not messages:
        return ""

    for msg in reversed(messages):
        if (msg.role or "user").lower() != "user":
            continue

        content = msg.content
        if isinstance(content, str) and content.strip():
            return content

        if isinstance(content, list):
            text_parts = [
                part.get("text", "")
                for part in content
                if isinstance(part, dict) and part.get("type") == "text"
            ]
            text = "\n".join(part for part in text_parts if part.strip())
            if text:
                return text

    return ""

@app.get("/")
def root():
    return {
        "status": "online",
        "description": "LangGraph Multi-Model Router is running.",
        "endpoints": ["/chat", "/collaborate", "/v1/chat/completions", "/v1/completions", "/v1/models", "/stats", "/health", "/docs"]
    }


@app.get("/health")
def health_check():
    """Check Ollama connectivity and list loaded models."""
    import subprocess
    try:
        result = subprocess.run(
            ["ollama", "list"],
            capture_output=True, text=True, timeout=10
        )
        models = []
        for line in result.stdout.strip().split("\n")[1:]:
            parts = line.split()
            if parts:
                models.append({
                    "name": parts[0],
                    "size": parts[1] if len(parts) > 1 else "unknown",
                    "modified": parts[2] if len(parts) > 2 else "unknown"
                })
        return {"status": "ok", "ollama": "connected", "models": models}
    except subprocess.TimeoutExpired:
        return {"status": "error", "ollama": "timeout", "models": []}
    except FileNotFoundError:
        return {"status": "error", "ollama": "not found", "models": []}
    except Exception as e:
        return {"status": "error", "ollama": str(e), "models": []}

@app.get("/v1/models")
def list_models():
    return {
        "object": "list",
        "data": [
            {"id": "langgraph-router", "object": "model", "owned_by": "local-router"},
            {"id": "langgraph-collaborative", "object": "model", "owned_by": "local-collaborative", "description": "Multi-agent: Coder + Critic pair"},
            {"id": "coder-architect:latest", "object": "model", "owned_by": "ollama"},
            {"id": "qwen2.5-coder:3b", "object": "model", "owned_by": "ollama"}
        ]
    }

@app.post("/chat")
def chat_endpoint(req: ChatRequest, auth_token: str = Depends(verify_api_key)):
    try:
        result = _run_router(
            query=req.query,
            image_path=req.image_path,
            history=req.history
        )
        return ChatResponse(
            category=result["category"],
            model_used=result["model_used"],
            response=result["response"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stats")
def get_stats(flush: bool = False):
    """Return self-learning statistics. Set flush=true to sync experiences to training buffer."""
    import os
    exp_file = os.path.join(os.path.dirname(__file__), "self_learning", "experiences.jsonl")
    if not os.path.exists(exp_file):
        return {"total": 0, "by_model": {}, "by_category": {}, "buffer_samples": 0}

    by_model = {}
    by_category = {}
    total = 0
    with open(exp_file, "r", encoding="utf-8") as f:
        for line in f:
            try:
                record = json.loads(line)
                total += 1
                model = record.get("model_used", "unknown")
                cat = record.get("category", "unknown")
                by_model[model] = by_model.get(model, 0) + 1
                by_category[cat] = by_category.get(cat, 0) + 1
            except Exception:
                continue

    # Flush to training buffer if requested
    buffer_samples = 0
    if flush:
        try:
            from self_learning.continuous_learning_buffer import sync_experiences_to_training_buffer
            buffer_samples = sync_experiences_to_training_buffer()
        except Exception as e:
            return {"error": f"flush failed: {str(e)}"}

    return {"total": total, "by_model": by_model, "by_category": by_category, "buffer_samples": buffer_samples}


@app.post("/collaborate")
def collaborate_endpoint(req: ChatRequest, auth_token: str = Depends(verify_api_key)):
    """Trigger the collaborative multi-agent workflow (Draft -> Critique -> Refine + RAG)."""
    try:
        initial_state = {
            "query": req.query,
            "context": "",
            "draft": "",
            "critique": "",
            "final_response": "",
            "model_used": ""
        }
        result = collaborative_graph.invoke(initial_state)
        return ChatResponse(
            category="collaborative",
            model_used=result["model_used"],
            response=result["final_response"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/v1/completions")
def legacy_completions(req: Dict[str, Any]):
    """Support Continue's legacy OpenAI completion endpoint."""
    try:
        user_query = _extract_prompt(req.get("prompt"))
        result = _run_router(user_query)
        completion_id = "cmpl-langgraph-router"
        created = int(time.time())
        model = result["model_used"]
        text = result["response"]

        if req.get("stream"):
            def event_stream():
                chunk = {
                    "id": completion_id,
                    "object": "text_completion",
                    "created": created,
                    "model": model,
                    "choices": [{"text": text, "index": 0, "logprobs": None, "finish_reason": None}]
                }
                yield f"data: {json.dumps(chunk)}\n\n"
                final_chunk = {
                    "id": completion_id,
                    "object": "text_completion",
                    "created": created,
                    "model": model,
                    "choices": [{"text": "", "index": 0, "logprobs": None, "finish_reason": "stop"}]
                }
                yield f"data: {json.dumps(final_chunk)}\n\n"
                yield "data: [DONE]\n\n"

            return StreamingResponse(event_stream(), media_type="text/event-stream")

        return {
            "id": completion_id,
            "object": "text_completion",
            "created": created,
            "model": model,
            "choices": [{"text": text, "index": 0, "logprobs": None, "finish_reason": "stop"}],
            "usage": {
                "prompt_tokens": len(user_query.split()),
                "completion_tokens": len(text.split()),
                "total_tokens": len(user_query.split()) + len(text.split())
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/chat/completions")
def openai_compatible_chat(req: OpenAIChatRequest):
    try:
        user_query = _extract_last_user_message(req.messages)

        if not user_query and req.prompt:
            user_query = str(req.prompt)

        if not user_query:
            user_query = "Please complete or analyze the selected code."

        result = _run_router(user_query)
        if req.stream:
            completion_id = "chatcmpl-langgraph-router"
            created = int(time.time())
            model = result["model_used"]
            text = result["response"]

            def event_stream():
                first_chunk = {
                    "id": completion_id,
                    "object": "chat.completion.chunk",
                    "created": created,
                    "model": model,
                    "choices": [{
                        "index": 0,
                        "delta": {"role": "assistant", "content": text},
                        "finish_reason": None
                    }]
                }
                yield f"data: {json.dumps(first_chunk)}\n\n"
                final_chunk = {
                    "id": completion_id,
                    "object": "chat.completion.chunk",
                    "created": created,
                    "model": model,
                    "choices": [{
                        "index": 0,
                        "delta": {},
                        "finish_reason": "stop"
                    }]
                }
                yield f"data: {json.dumps(final_chunk)}\n\n"
                yield "data: [DONE]\n\n"

            return StreamingResponse(event_stream(), media_type="text/event-stream")

        return {
            "id": "chatcmpl-langgraph-router",
            "object": "chat.completion",
            "model": result["model_used"],
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": result["response"]
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": len(user_query.split()),
                "completion_tokens": len(result["response"].split()),
                "total_tokens": len(user_query.split()) + len(result["response"].split())
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8001)
