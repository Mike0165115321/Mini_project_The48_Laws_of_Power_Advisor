# main.py (Final Full-Stack Version)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, FileResponse 
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os

from core.rag_engine import RAGEngine
from core.power_advisor import PowerAdvisor
from core.api_key_manager import ApiKeyManager
from core.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("--- 🚀 เริ่มต้นการทำงานของ Advisor API ---")
    app.state.key_manager = ApiKeyManager(all_google_keys=settings.GOOGLE_API_KEYS)
    app.state.rag_engine = RAGEngine(book_index_path="data/index")
    app.state.power_advisor = PowerAdvisor(
        rag_engine=app.state.rag_engine,
        key_manager=app.state.key_manager
    )
    print("--- ✅ ระบบพร้อมให้บริการ ---")
    yield
    print("--- 🌙 ปิดการทำงานของระบบ ---")

app = FastAPI(title="The 48 Laws of Power Advisor API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_folder = os.path.join(os.path.dirname(__file__), "static")
app.mount("/static", StaticFiles(directory=static_folder), name="static")

# --- Endpoints ---
@app.get("/", response_class=FileResponse, tags=["Frontend"])
def read_root():
    """
    Endpoint หลักสำหรับให้บริการหน้า index.html
    """
    return os.path.join(static_folder, "index.html")

@app.get("/ask", tags=["API"])
async def ask_advisor_stream(query: str):
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    advisor: PowerAdvisor = app.state.power_advisor
    return StreamingResponse(advisor.answer_stream(query), media_type="text/event-stream")