import jwt
import asyncio
from datetime import datetime, timedelta

from backend.rbac.middleware import enforce_rbac, SECRET_KEY, ALGORITHM

def create_token(username, role, department):
    payload = {
        "sub": username,
        "role": role,
        "department": department,
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

class MockRequest:
    def __init__(self, token):
        self.headers = {
            "Authorization": f"Bearer {token}"
        }

async def run_tests():
    print("\n=== RBAC TEST RUNNER STARTED ===\n")

    users = [
        ("Ritika", "C-Level", "Finance", "Finance", "Financial report", "ALLOWED"),
        ("Rahul", "HR", "HR", "Finance", "Finance salaries", "DENIED"),
        ("Anita", "Engineering", "Engineering", "Engineering", "System design", "ALLOWED"),
        ("Karan", "Marketing", "Marketing", "HR", "HR policies", "DENIED"),
    ]

    for username, role, user_dept, req_dept, query, expected in users:
        token = create_token(username, role, user_dept)
        request = MockRequest(token)

        try:
            await enforce_rbac(
                request,
                action="Search",
                dept_requested=req_dept,
                query=query
            )
            result = "ALLOWED"
        except Exception:
            result = "DENIED"

        print(
            f"User: {username} | Role: {role} | "
            f"Dept: {user_dept} | Requested: {req_dept} | "
            f"Query: '{query}' | Result: {result} | Expected: {expected}"
        )

    print("\n=== RBAC TEST RUNNER COMPLETED ===\n")

if __name__ == "__main__":
    asyncio.run(run_tests())
