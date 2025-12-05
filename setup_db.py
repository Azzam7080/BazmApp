# setup_db.py
from data.database import get_connection

def init_db():
    conn = get_connection()
    c = conn.cursor()
    
    # Users
    c.execute("""CREATE TABLE IF NOT EXISTS users(
        email TEXT PRIMARY KEY, name TEXT, role TEXT, 
        password_hash TEXT, has_oath INTEGER DEFAULT 0)""")
    
    # Events
    c.execute("""CREATE TABLE IF NOT EXISTS events(
        id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, 
        description TEXT, datetime TEXT, location TEXT, created_by TEXT)""")
    
    # Registrations
    c.execute("""CREATE TABLE IF NOT EXISTS registrations(
        id INTEGER PRIMARY KEY AUTOINCREMENT, event_id INTEGER, 
        user_email TEXT, UNIQUE(event_id, user_email))""")
    
    # Reports (Version 3: Added month, year, structured_data)
    c.execute("""CREATE TABLE IF NOT EXISTS reports(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        month TEXT,
        year TEXT,
        structured_data TEXT,  -- Stores the entire form as JSON
        author_email TEXT,
        created_at TEXT
    )""")
    
    conn.commit()
    conn.close()
    print("Database initialized (Version 3: Complex Reports)!")

if __name__ == "__main__":
    init_db()