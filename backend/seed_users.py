import sqlite3
import os

# Import from parent directory when run directly
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.auth.auth_handler import hash_password
from backend.database import create_user_table, get_connection

def seed_all_users():
    """
    Create all default users in the database
    Run this to initialize users permanently
    """
    # Step 1: Force table creation first
    create_user_table()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Define all default users
    users = [
        {
            "username": "admin",
            "password": "admin123",
            "role": "admin",
            "department": "C level"
        },
        {
            "username": "ritika",
            "password": "ritika123",
            "role": "Finance",
            "department": "Finance"
        },
        {
            "username": "keerthi",
            "password": "keerthi123",
            "role": "engineer",
            "department": "Engineering"
        },
        {
            "username": "kanak",
            "password": "kanak123",
            "role": "marketing_analyst",
            "department": "Marketing"
        }
    ]
    
    # Insert all users (INSERT OR REPLACE will update if exists)
    for user in users:
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO users (username, password, role, department)
                VALUES (?, ?, ?, ?)
            """, (
                user["username"],
                hash_password(user["password"]),
                user["role"],
                user["department"]
            ))
            print(f"[OK] User '{user['username']}' created/updated")
        except Exception as e:
            print(f"[ERROR] Error creating user '{user['username']}': {e}")
    
    conn.commit()
    
    # Display all users
    cursor.execute("SELECT id, username, role, department FROM users")
    rows = cursor.fetchall()
    
    print("\n" + "=" * 60)
    print("DATABASE USERS (PERMANENT)")
    print("=" * 60)
    print(f"{'ID':<5} {'Username':<15} {'Role':<20} {'Department'}")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]:<5} {row[1]:<15} {row[2]:<20} {row[3]}")
    print("-" * 60)
    print(f"Total Users: {len(rows)}")
    print("=" * 60)
    
    conn.close()
    print("\n[SUCCESS] All users have been seeded permanently!")

if __name__ == "__main__":
    seed_all_users()
