import sqlite3
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['pbkdf2_sha256'], deprecated='auto')

def hash_password(password):
    return pwd_context.hash(password)

db_path = 'c:/Users/kanak/OneDrive/Documents/RBAC-GROUP-2/users.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Delete existing admin
cursor.execute('DELETE FROM users WHERE username = ?', ('admin',))

# Recreate admin with correct role and department
cursor.execute('''
    INSERT INTO users (username, password, role, department)
    VALUES (?, ?, ?, ?)
''', ('admin', hash_password('admin123'), 'C-Level', 'General'))

conn.commit()

# Verify
cursor.execute('SELECT id, username, role, department FROM users')
users = cursor.fetchall()
conn.close()

print('=== Users in Database ===')
for u in users:
    print(f"ID={u[0]}, Username={u[1]}, Role={u[2]}, Department={u[3]}")
