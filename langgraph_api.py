"""
FastAPI Server exposing the LangGraph Multi-Model Router.
Endpoint: POST /chat or POST /v1/chat/completions (OpenAI-compatible)
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
from langgraph_router import app as router_graph

app = FastAPI(
    title="LangGraph Local Multi-Model API",
    description="Unified API routing queries between General, Quick Code, Architecture, Reasoning, and Vision local models.",
    version="1.0.0"
)

# Request schema for direct chat
class ChatRequest(BaseModel):
    query: str
    image_path: Optional[str] = None

class ChatResponse(BaseModel):
    category: str
    model_used: str
    response: str

# OpenAI-compatible schemas
class OpenAIMessage(BaseModel):
    role: str
    content: Any

class OpenAIChatRequest(BaseModel):
    model: Optional[str] = "langgraph-router"
    messages: List[OpenAIMessage]
    temperature: Optional[float] = 0.7

@app.get("/")
def root():
    return {
        "status": "online",
        "description": "LangGraph Multi-Model Router is running.",
        "endpoints": ["/chat", "/v1/chat/completions", "/docs"]
    }

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    """Direct JSON endpoint to route user query."""
    try:
        initial_state = {
            "query": req.query,
            "image_path": req.image_path,
            "category": "general",
            "response": "",
            "model_used": ""
        }
        result = router_graph.invoke(initial_state)
        return ChatResponse(
            category=result["category"],
            model_used=result["model_used"],
            response=result["response"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/v1/chat/completions")
def openai_compatible_chat(req: OpenAIChatRequest):
    """OpenAI-compatible /v1/chat/completions endpoint for VS Code / Open-WebUI / Cursor."""
    try:
        # Extract last user query
        user_query = ""
        for msg in reversed(req.messages):
            if msg.role == "user":
                if isinstance(msg.content, str):
                    user_query = msg.content
                elif isinstance(msg.content, list):
                    # Extract text from multimodal payload
                    for part in msg.content:
                        if isinstance(part, dict) and part.get("type") == "text":
                            user_query = part.get("text", "")
                break

        if not user_query:
            user_query = "Hello"

        initial_state = {
            "query": user_query,
            "image_path": None,
            "category": "general",
            "response": "",
            "model_used": ""
        }
        result = router_graph.invoke(initial_state)

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
    print("Starting LangGraph API Server on http://localhost:8000 (docs: http://localhost:8000/docs)")
    uvicorn.run(app, host="127.0.0.1", port=8000)
