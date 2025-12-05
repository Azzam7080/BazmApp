# fix_db.py
from data.database import get_connection

def add_announcements():
    conn = get_connection()
    c = conn.cursor()
    # Create the missing table
    c.execute("""CREATE TABLE IF NOT EXISTS announcements(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        title TEXT, 
        content TEXT, 
        created_at TEXT
    )""")
    conn.commit()
    conn.close()
    print("Fixed! Announcements table added.")

if __name__ == "__main__":
    add_announcements()