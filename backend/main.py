from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from backend.models import User
from backend.database import get_connection, create_user_table
from backend.seed_users import seed_all_users
from backend.auth.auth_handler import hash_password
from backend.auth.auth_bearer import get_current_user
from backend.auth.login import router as login_router
from scripts.search.semantic_search import semantic_search

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path=env_path)
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

# Auth routes
app.include_router(login_router)

# Initialize database and seed users
create_user_table()
seed_all_users()


@app.get("/")
def health_check():
    return {"status": "Backend running"}


@app.post("/users")
def create_user(user: User):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        if len(user.password.encode("utf-8")) > 72:
            raise HTTPException(status_code=400, detail="Password too long")

        cursor.execute(
            """
            INSERT OR REPLACE INTO users (username, password, role, department)
            VALUES (?, ?, ?, ?)
            """,
            (
                user.username,
                hash_password(user.password),
                user.role,
                user.department,
            ),
        )
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        conn.close()

    return {"status": "User created successfully"}


@app.get("/users")
def get_users(current_user=Depends(get_current_user)):
    return {"detail": "Authorized"}


@app.post("/chat")
async def chat(request: ChatRequest, current_user=Depends(get_current_user)):
    # Check for at least one LLM provider
    hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
    groq_key = os.getenv("GROQ_API_KEY")
    use_ollama = os.getenv("USE_OLLAMA", "false").lower() == "true"
    
    if not hf_token and not groq_key and not use_ollama:
        raise HTTPException(
            status_code=500,
            detail="No LLM configured. Set USE_OLLAMA=true, GROQ_API_KEY, or HUGGINGFACE_API_TOKEN in .env",
        )

    try:
        from backend.rag.pipeline import run_rag_pipeline
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline import error: {str(e)}",
        )

    try:
        search_results = semantic_search(request.query, top_k=10)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search error: {str(e)}",
        )

    return run_rag_pipeline(
        current_user,
        request.query,
        search_results=search_results,
    )
