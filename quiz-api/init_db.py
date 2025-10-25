import os
import sqlite3
DB_PATH = "DB_quiz.db"

def create_db():
    abs_path = os.path.abspath(DB_PATH)
    print(f"[init_db] create_db called. DB will be at: {abs_path}")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Answer")
    cur.execute("DROP TABLE IF EXISTS Participation")
    cur.execute("DROP TABLE IF EXISTS Question")
    cur.execute("DROP TABLE IF EXISTS Log")
    cur.execute("""
        CREATE TABLE Question (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            position INTEGER UNIQUE,
            title TEXT,
            text TEXT,
            image TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE Answer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER,
            text TEXT,
            isCorrect INTEGER,
            FOREIGN KEY(question_id) REFERENCES Question(id) ON DELETE CASCADE
        )
    """)
    cur.execute("""
        CREATE TABLE Participation (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            playerName TEXT,
            score INTEGER
        )
    """)
    cur.execute("""
        CREATE TABLE Log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user TEXT,
            action TEXT,
            endpoint TEXT,
            status TEXT,
            details TEXT
        )
    """)
    conn.commit()
    conn.close()
    
def create_log_table():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            user TEXT,
            action TEXT,
            endpoint TEXT,
            status TEXT,
            details TEXT
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()