# data/database.py
import sqlite3

DB_FILE = "bazm_app.db"

def get_connection():
    """Returns a connection to the SQLite database."""
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def execute_query(query, params=()):
    """Executes a query (INSERT, UPDATE, DELETE) and commits changes."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
    finally:
        conn.close()

def fetch_all(query, params=()):
    """Executes a SELECT query and returns all rows."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchall()
    finally:
        conn.close()

def fetch_one(query, params=()):
    """Executes a SELECT query and returns a single row."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return cursor.fetchone()
    finally:
        conn.close()