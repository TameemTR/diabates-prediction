import sqlite3
import hashlib

# Connect to SQLite database
conn = sqlite3.connect("data/users.db", check_same_thread=False)
cursor = conn.cursor()

# Create users table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT
    )
''')
conn.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    if not username or not password:
        return False
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        return False
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                   (username, hash_password(password)))
    conn.commit()
    return True

def login_user(username, password):
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", 
                   (username, hash_password(password)))
    return cursor.fetchone() is not None
