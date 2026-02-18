import sqlite3
import os

db_path = "users.db"
full_path = os.path.join(os.path.dirname(__file__), db_path)
print(f"Using database: {full_path}")

conn = sqlite3.connect(full_path)
cursor = conn.cursor()

cursor.execute("SELECT username, role, department FROM users")
users = cursor.fetchall()
print("All users in database:")
for user in users:
    print(f"  - {user[0]}: role={user[1]}, department={user[2]}")

conn.close()
