from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.models import User
from backend.database import get_connection, create_user_table
from backend.auth.auth_bearer import get_current_user 
from backend.auth.login import router as login_router
from backend.auth.auth_handler import hash_password
from dotenv import load_dotenv
import os

# Load .env from the backend folder
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")
if not HF_TOKEN:
    raise RuntimeError("Hugging Face API token not found. Please set HUGGINGFACE_API_TOKEN in backend/.env")

try:
    from backend.rag.pipeline import run_rag_pipeline
except ImportError:
    run_rag_pipeline = None

class ChatRequest(BaseModel):
    query: str

app = FastAPI(title="RBAC Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login_router)

create_user_table()

@app.post("/users")
def create_user(user: User):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if len(user.password.encode("utf-8")) > 72:
            raise HTTPException(status_code=400, detail="Password too long")
        password_to_save = hash_password(user.password)
        cursor.execute(
            "INSERT OR REPLACE INTO users (username, password, role, department) VALUES (?, ?, ?, ?)",
            (user.username, password_to_save, user.role, user.department)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()
    return {"status": "User created successfully"}

from scripts.search.semantic_search import semantic_search # Add this import at the top

@app.post("/chat")
async def chat(request: ChatRequest, current_user=Depends(get_current_user)):
    user = current_user
    question = request.query
    
    # This fetches the ACTUAL data from ChromaDB
    try:
        results = semantic_search(question)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search Error: {str(e)}")

    if run_rag_pipeline is None:
        return {"answer": "Pipeline Error", "sources": []}

    # Pass the real results to the pipeline
    response = run_rag_pipeline(user, question, search_results=results)
    return response
