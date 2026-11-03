"""Local API. Binds only to loopback; no arbitrary shell execution is exposed."""
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from .config import settings
from .providers import ProviderError, complete
from .storage import Store

store: Store

@asynccontextmanager
async def lifespan(_: FastAPI):
    global store
    store = Store(settings.database_path)
    settings.workspace.mkdir(parents=True, exist_ok=True)
    yield

app = FastAPI(title="SMERKA local service", version="0.1.0", lifespan=lifespan)

class ChatRequest(BaseModel):
    conversation_id: str = Field(min_length=1, max_length=80, pattern=r"^[a-zA-Z0-9_-]+$")
    message: str = Field(min_length=1, max_length=12000)

class ChatResponse(BaseModel):
    conversation_id: str
    reply: str

@app.get("/health")
async def health():
    return {"status": "ok", "provider": settings.provider, "model": settings.model}

@app.get("/conversations/{conversation_id}")
async def history(conversation_id: str):
    if not conversation_id or len(conversation_id) > 80:
        raise HTTPException(400, "Invalid conversation id")
    return {"messages": store.recent(conversation_id, limit=100)}

@app.delete("/conversations/{conversation_id}")
async def clear(conversation_id: str):
    store.clear(conversation_id)
    return {"cleared": True}

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    store.append(request.conversation_id, "user", request.message)
    history_messages = store.recent(request.conversation_id, limit=20)
    messages = [{"role": m["role"], "content": m["content"]} for m in history_messages]
    try:
        reply = await complete(settings, messages)
    except ProviderError as exc:
        # Do not fake a model response or log secret-bearing provider payloads.
        raise HTTPException(503, str(exc)) from exc
    store.append(request.conversation_id, "assistant", reply)
    return ChatResponse(conversation_id=request.conversation_id, reply=reply)
