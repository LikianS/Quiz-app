import sqlite3

DB_PATH = "DB_quiz.db"

def create_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS Answer")
    cur.execute("DROP TABLE IF EXISTS Participation")
    cur.execute("DROP TABLE IF EXISTS Question")
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
    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()