import sqlite3
from backend.auth.auth_handler import hash_password
from backend.database import create_user_table, get_connection

def create_admin():
    # Step 1: Force the table creation first
    create_user_table()
    
    conn = get_connection()
    cursor = conn.cursor()

    # Step 2: Insert the admin
    cursor.execute("""
    INSERT OR IGNORE INTO users (username, password, role, department)
    VALUES (?, ?, ?, ?)
    """, (
        "admin",
        hash_password("admin123"),
        "C-Level",  
        "Executive" 
    ))

    conn.commit()
    conn.close()
    print("✅ Admin user created successfully")

if __name__ == "__main__":
    create_admin()
