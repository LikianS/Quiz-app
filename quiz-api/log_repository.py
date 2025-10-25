import sqlite3
from datetime import datetime
from zoneinfo import ZoneInfo


DB_PATH = "DB_quiz.db"

def insert_log(user, action, endpoint, status, details=""):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    dt = datetime.now(ZoneInfo("Europe/Paris"))

    cur.execute(
        "INSERT INTO Log (timestamp, user, action, endpoint, status, details) VALUES (?, ?, ?, ?, ?, ?)",
        (dt.isoformat(), user, action, endpoint, status, details)
    )
    conn.commit()
    conn.close()

def get_logs():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT timestamp, user, action, endpoint, status, details FROM Log ORDER BY timestamp DESC")
    logs = [
        {
            "timestamp": row[0],
            "user": row[1],
            "action": row[2],
            "endpoint": row[3],
            "status": row[4],
            "details": row[5]
        }
        for row in cur.fetchall()
    ]
    conn.close()
    return logs
