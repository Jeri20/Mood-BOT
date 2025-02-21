import sqlite3
import hashlib

DB_PATH = "data/mood_tracker.db"

def create_tables():
    """Initialize the database with users and moods tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS moods (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT,
                        date TEXT,
                        mood TEXT,
                        FOREIGN KEY(username) REFERENCES users(username))''')

    conn.commit()
    conn.close()

def hash_password(password):
    """Hash a password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(username, password):
    """Register a new user."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                       (username, hash_password(password)))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False  # Username already exists

def authenticate_user(username, password):
    """Authenticate user credentials."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT password FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    
    conn.close()
    
    if result and result[0] == hash_password(password):
        return True
    return False

def save_mood(username, date, mood):
    """Save user mood in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("INSERT INTO moods (username, date, mood) VALUES (?, ?, ?)", 
                   (username, date, mood))
    
    conn.commit()
    conn.close()

def get_moods(username):
    """Retrieve user mood history."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT date, mood FROM moods WHERE username=? ORDER BY date DESC", (username,))
    moods = cursor.fetchall()
    
    conn.close()
    return moods

# Initialize the database on first run
create_tables()
