import sqlite3
from question_model import Question

DB_PATH = "DB_quiz.db"

def insert_question(question: Question):
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM Question WHERE position = ?", (question.position,))
        if cur.fetchone():
            raise Exception("Position already used by another question")
        cur.execute(
            "INSERT INTO Question (position, title, text, image) VALUES (?, ?, ?, ?)",
            (question.position, question.title, question.text, question.image)
        )
        qid = cur.lastrowid
        for answer in question.possibleAnswers:
            cur.execute(
                "INSERT INTO Answer (question_id, text, isCorrect) VALUES (?, ?, ?)",
                (qid, answer['text'], int(answer['isCorrect']))
            )
        conn.commit()
        return qid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_possible_answers(qid):
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cur = conn.cursor()
    cur.execute("SELECT text, isCorrect FROM Answer WHERE question_id = ?", (qid,))
    rows = cur.fetchall()
    conn.close()
    return [{"text": row[0], "isCorrect": bool(row[1])} for row in rows]

def get_question_by_id(qid):
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cur = conn.cursor()
    cur.execute("SELECT id, position, title, text, image FROM Question WHERE id = ?", (qid,))
    row = cur.fetchone()
    conn.close()
    if row:
        possibleAnswers = get_possible_answers(row[0])
        return Question(position=row[1], title=row[2], text=row[3], image=row[4], possibleAnswers=possibleAnswers, id=row[0])
    return None

def get_question_by_position(position):
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cur = conn.cursor()
    cur.execute("SELECT id, position, title, text, image FROM Question WHERE position = ?", (position,))
    row = cur.fetchone()
    conn.close()
    if row:
        possibleAnswers = get_possible_answers(row[0])
        return Question(position=row[1], title=row[2], text=row[3], image=row[4], possibleAnswers=possibleAnswers, id=row[0])
    return None

def update_question(question: Question):
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cur = conn.cursor()
    question_id_int = int(question.id) if question.id is not None else None

    cur.execute(
        "SELECT id FROM Question WHERE position=? AND id!=?",
        (question.position, question_id_int)
    )
    row = cur.fetchone()
    if row is not None and row[0] != question_id_int:
        conn.close()
        raise Exception("Position already used by another question")

    cur.execute("DELETE FROM Answer WHERE question_id = ?", (question_id_int,))
    cur.execute(
        "UPDATE Question SET title=?, text=?, image=?, position=? WHERE id=?",
        (question.title, question.text, question.image, question.position, question_id_int)
    )
    for answer in question.possibleAnswers:
        cur.execute(
            "INSERT INTO Answer (question_id, text, isCorrect) VALUES (?, ?, ?)",
            (question_id_int, answer['text'], int(answer['isCorrect']))
        )
    conn.commit()
    conn.close()

def delete_question_by_id(qid):
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cur = conn.cursor()
    cur.execute("DELETE FROM Answer WHERE question_id = ?", (qid,))
    cur.execute("DELETE FROM Question WHERE id = ?", (qid,))
    conn.commit()
    conn.close()

def delete_all_questions():
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cur = conn.cursor()
    cur.execute("DELETE FROM Answer")
    cur.execute("DELETE FROM Question")
    conn.commit()
    conn.close()

def get_questions_count():
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM Question")
    count = cur.fetchone()[0]
    conn.close()
    return count