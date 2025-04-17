import bcrypt
import sqlite3

def insert_user(username, password, role):
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)",
              (username, password_hash, role))
    conn.commit()
    conn.close()

# Example: Insert a sample HR user
insert_user('hr_user', 'hr_password', 'hr')
