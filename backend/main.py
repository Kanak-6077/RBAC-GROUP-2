from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from backend.models import User
from backend.database import get_connection, create_user_table
from backend.auth.auth_handler import hash_password
from backend.auth.auth_bearer import get_current_user
from backend.auth.login import router as login_router
from scripts.search.semantic_search import semantic_search

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


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

# Initialize database
create_user_table()


def ensure_test_user():
    """
    Create default admin user for runtime only.
    Skipped during pytest to avoid bcrypt initialization at import time.
    """
    if os.getenv("PYTEST_RUNNING") == "1":
        return

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT 1 FROM users WHERE username = ?",
        ("admin",),
    )

    if not cursor.fetchone():
        cursor.execute(
            """
            INSERT INTO users (username, password, role, department)
            VALUES (?, ?, ?, ?)
            """,
            (
                "admin",
                hash_password("admin123"),
                "C-Level",
                "General",
            ),
        )
        conn.commit()

    conn.close()


# Safe to call (no effect during tests)
ensure_test_user()


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
    if not os.getenv("HUGGINGFACE_API_TOKEN"):
        raise HTTPException(
            status_code=500,
            detail="Hugging Face API token not configured",
        )

    try:
        from backend.rag.pipeline import run_rag_pipeline
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline import error: {str(e)}",
        )

    try:
        search_results = semantic_search(request.query)
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
