import sqlite3
import uuid
from datetime import datetime
from config.settings import DB_PATH

def init_db():
    """Initializes the SQLite database tables."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            title TEXT,
            created_at TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            role TEXT,
            content TEXT,
            image_url TEXT,
            timestamp TIMESTAMP,
            FOREIGN KEY(session_id) REFERENCES sessions(id)
        )
    ''')
    conn.commit()
    conn.close()

def create_session(title: str) -> str:
    """Creates a new chat session."""
    session_id = str(uuid.uuid4())
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO sessions (id, title, created_at) VALUES (?, ?, ?)", 
              (session_id, title, datetime.now()))
    conn.commit()
    conn.close()
    return session_id

def add_message(session_id: str, role: str, content: str, image_url: str = None):
    """Saves a message (and optional image URL) to the DB."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO messages (session_id, role, content, image_url, timestamp) VALUES (?, ?, ?, ?, ?)",
              (session_id, role, content, image_url, datetime.now()))
    conn.commit()
    conn.close()

def get_sessions():
    """Fetches all sessions, newest first."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM sessions ORDER BY created_at DESC")
    return c.fetchall()

def get_history(session_id: str):
    """Fetches full chat history for a session."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM messages WHERE session_id = ? ORDER BY timestamp ASC", (session_id,))
    return c.fetchall()