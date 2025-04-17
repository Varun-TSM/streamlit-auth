import sqlite3
from typing import Optional

DB_NAME = "user_auth.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Create tables for each role
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS interviewer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS valid_candidate_emails (
            email TEXT PRIMARY KEY
        )
    ''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS hr (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            access_code TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()


def create_user(role: str, email: str, credential: str) -> bool:
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        if role == "interviewer":
            cursor.execute("INSERT INTO interviewer (email, password) VALUES (?, ?)", (email, credential))
        elif role == "candidate":
            cursor.execute("INSERT INTO candidate (email, candidate_id) VALUES (?, ?)", (email, credential))
        elif role == "hr":
            cursor.execute("INSERT INTO hr (email, access_code) VALUES (?, ?)", (email, credential))

        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False  # Email already exists
    finally:
        conn.close()


def verify_user(role: str, email: str, credential: str) -> bool:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    query = ""
    if role == "interviewer":
        query = "SELECT * FROM interviewer WHERE email = ? AND password = ?"
    elif role == "candidate":
        query = "SELECT * FROM candidate WHERE email = ? AND candidate_id = ?"
    elif role == "hr":
        query = "SELECT * FROM hr WHERE email = ? AND access_code = ?"

    cursor.execute(query, (email, credential))
    result = cursor.fetchone()

    conn.close()
    return result is not None


def user_exists(role: str, email: str) -> bool:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    query = f"SELECT 1 FROM {role} WHERE email = ?"
    cursor.execute(query, (email,))
    result = cursor.fetchone()

    conn.close()
    return result is not None

def is_valid_candidate_email(email: str) -> bool:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM valid_candidate_emails WHERE email = ?", (email,))
    result = cursor.fetchone()

    conn.close()
    return result is not None
