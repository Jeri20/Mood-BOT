import sqlite3
import hashlib
from datetime import datetime

DB_PATH = "data/mood_tracker.db"

def create_tables():
    """Initialize the database with users, questionnaire responses, and moods."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Users Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT)''')

    # Questionnaire Responses Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS questionnaire (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        phq9_score INTEGER,
                        gad7_score INTEGER,
                        FOREIGN KEY(username) REFERENCES users(username))''')

    # Moods Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS moods (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT NOT NULL,
                        mood TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY(username) REFERENCES users(username))''')

    conn.commit()
    conn.close()

def hash_password(password):
    """Hash a password for security."""
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

    if result:
        stored_hash = result[0]
        entered_hash = hash_password(password)

        if stored_hash == entered_hash:
            return True  # Successful login
    return False  # Login failed

def save_questionnaire(username, phq9_score, gad7_score):
    """Save user PHQ-9 and GAD-7 questionnaire scores."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        cursor.execute("INSERT INTO questionnaire (username, phq9_score, gad7_score) VALUES (?, ?, ?)",
                       (username, phq9_score, gad7_score))
    except sqlite3.IntegrityError:
        cursor.execute("UPDATE questionnaire SET phq9_score=?, gad7_score=? WHERE username=?", 
                       (phq9_score, gad7_score, username))
    
    conn.commit()
    conn.close()

def get_questionnaire_scores(username):
    """Retrieve questionnaire scores for a user."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT phq9_score, gad7_score FROM questionnaire WHERE username=?", (username,))
    scores = cursor.fetchone()
    conn.close()
    return scores if scores else (None, None)

def save_mood(username, mood):
    """Save user's mood entry."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO moods (username, mood, timestamp) VALUES (?, ?, ?)", 
                   (username, mood, timestamp))
    
    conn.commit()
    conn.close()

def get_moods(username):
    """Retrieve mood history for a user."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT mood, timestamp FROM moods WHERE username=? ORDER BY timestamp DESC", (username,))
    moods = cursor.fetchall()
    conn.close()
    return moods

# Initialize database
create_tables()
