from fastapi import FastAPI, HTTPException
from backend.models import User
from backend.database import get_connection, create_user_table
from fastapi import Depends
from backend.auth.auth import get_current_user
from backend.auth.login import router as login_router
from backend.auth.auth_handler import hash_password

from fastapi.middleware.cors import CORSMiddleware
from backend.rbac.middleware import enforce_rbac
from backend.rag.pipeline import run_rag_pipeline

app = FastAPI(title="RBAC Backend")
app.include_router(login_router)
create_user_table()

@app.post("/users")
def create_user(user: User):
    conn = get_connection()
    cursor = conn.cursor()

    # Check password byte length (bcrypt limit is 72 bytes)
    try:
        if len(user.password.encode("utf-8")) > 72:
            raise HTTPException(status_code=400, detail="Password too long for encryption")
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=400, detail="Invalid password encoding")

    # Hash the password
    try:
        password_to_save = hash_password(user.password)
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail="Password hashing failed")

    # Insert user into database
    try:
        cursor.execute(
            "INSERT OR REPLACE INTO users (username, password, role, department) VALUES (?, ?, ?, ?)",
            (user.username, password_to_save, user.role, user.department)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail="Database insert failed")
    finally:
        conn.close()

    return {"status": "User created successfully"}


@app.post("/chat")
async def chat(query: dict, request=Depends(get_current_user)):
    
    user = request
    question = query.get("question")

    if not question:
        raise HTTPException(status_code=400, detail="Question is required")

    # Enforce RBAC
    await enforce_rbac(
        request=request,
        action="Chat Query",
        dept_requested=user["department"]
    )

    response = run_rag_pipeline(user, question, search_results=[])

    return response
