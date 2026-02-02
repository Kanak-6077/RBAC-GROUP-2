"""
Script to create Kriti Sharma (Engineering) user profile
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.auth.auth_handler import hash_password
from backend.database import create_user_table, get_connection

def create_kriti_sharma_user():
    """Create Kriti Sharma user with Engineering role and department"""
    # Ensure table exists
    create_user_table()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Check if user already exists
    cursor.execute("SELECT * FROM users WHERE username = ?", ("kriti.sharma",))
    existing = cursor.fetchone()
    
    if existing:
        print("⚠️  User 'kriti.sharma' already exists. Updating...")
        cursor.execute("""
            UPDATE users 
            SET password = ?, role = ?, department = ?
            WHERE username = ?
        """, (
            hash_password("kriti123"),
            "Engineering",
            "Engineering",
            "kriti.sharma"
        ))
    else:
        print("➕ Creating new user 'kriti.sharma'...")
        cursor.execute("""
            INSERT INTO users (username, password, role, department)
            VALUES (?, ?, ?, ?)
        """, (
            "kriti.sharma",
            hash_password("kriti123"),
            "Engineering",
            "Engineering"
        ))
    
    conn.commit()
    
    # Verify user was created
    cursor.execute("SELECT username, role, department FROM users WHERE username = ?", ("kriti.sharma",))
    user = cursor.fetchone()
    
    conn.close()
    
    if user:
        print(f"✅ User created successfully:")
        print(f"   Username: {user[0]}")
        print(f"   Role: {user[1]}")
        print(f"   Department: {user[2]}")
        return True
    else:
        print("❌ Failed to create user")
        return False

if __name__ == "__main__":
    create_kriti_sharma_user()
