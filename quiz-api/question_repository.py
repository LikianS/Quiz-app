import sqlite3
from question_model import Question

DB_PATH = "DB_quiz.db"

def get_quiz_id(cur, quiz_name="default"):
    cur.execute("SELECT id FROM Quiz WHERE name = ?", (quiz_name,))
    quiz_row = cur.fetchone()
    if not quiz_row:
        cur.execute("INSERT INTO Quiz (name) VALUES (?)", (quiz_name,))
        return cur.lastrowid
    return quiz_row[0]

def insert_question(question: Question, quiz_name="default"):
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM Quiz WHERE name = ?", (quiz_name,))
        quiz_row = cur.fetchone()
        if not quiz_row:
            cur.execute("INSERT INTO Quiz (name) VALUES (?)", (quiz_name,))
            quiz_id = cur.lastrowid
        else:
            quiz_id = quiz_row[0]

        cur.execute("SELECT COUNT(*) FROM Question WHERE quiz_id = ?", (quiz_id,))
        count = cur.fetchone()[0]

        if question.position is None or question.position < 1:
            question.position = count + 1
        elif question.position > count + 1:
            question.position = count + 1

        cur.execute(
            "UPDATE Question SET position = position + 1000 WHERE quiz_id = ? AND position >= ?",
            (quiz_id, question.position)
        )

        cur.execute(
            "INSERT INTO Question (quiz_id, position, title, text, image) VALUES (?, ?, ?, ?, ?)",
            (quiz_id, question.position, question.title, question.text, question.image)
        )
        qid = cur.lastrowid

        for answer in question.possibleAnswers:
            cur.execute(
                "INSERT INTO Answer (question_id, text, isCorrect) VALUES (?, ?, ?)",
                (qid, answer['text'], int(answer['isCorrect']))
            )

        cur.execute(
            "UPDATE Question SET position = position - 999 WHERE quiz_id = ? AND position >= ?",
            (quiz_id, question.position + 1000)
        )

        conn.commit()
        return qid
    except Exception as e:
        conn.rollback()
        print("Erreur insert_question:", e)
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
        return Question(position=row[1], title=row[2], text=row[3], image=row[4],
                        possibleAnswers=possibleAnswers, id=row[0])
    return None

def get_question_by_position(position, quiz_name="default"):
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cur = conn.cursor()
    quiz_id = get_quiz_id(cur, quiz_name)
    cur.execute("SELECT id, position, title, text, image FROM Question WHERE quiz_id = ? AND position = ?", (quiz_id, position))
    row = cur.fetchone()
    conn.close()
    if row:
        possibleAnswers = get_possible_answers(row[0])
        return Question(position=row[1], title=row[2], text=row[3], image=row[4],
                        possibleAnswers=possibleAnswers, id=row[0])
    return None

def update_question(qid, title=None, text=None, image=None, possibleAnswers=None):
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cur = conn.cursor()
    try:
        if title is not None or text is not None or image is not None:
            cur.execute("UPDATE Question SET title = COALESCE(?, title), text = COALESCE(?, text), image = COALESCE(?, image) WHERE id = ?",
                        (title, text, image, qid))
        if possibleAnswers is not None:
            cur.execute("DELETE FROM Answer WHERE question_id = ?", (qid,))
            for ans in possibleAnswers:
                cur.execute("INSERT INTO Answer (question_id, text, isCorrect) VALUES (?, ?, ?)",
                            (qid, ans['text'], int(ans['isCorrect'])))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def _rewrite_sequential_positions(cur, ids_in_order):
    """
    Réécrit les positions 1..N pour les ids donnés dans l'ordre.
    Utilise un offset +1000 pour éviter les collisions UNIQUE.
    """
    cur.execute("UPDATE Question SET position = position + 1000")
    for new_pos, qid in enumerate(ids_in_order, start=1):
        cur.execute("UPDATE Question SET position = ? WHERE id = ?", (new_pos, qid))

def move_question(old_position, new_position):
    if old_position == new_position:
        return
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM Question ORDER BY position ASC")
        ids = [row[0] for row in cur.fetchall()]
        total = len(ids)
        if old_position < 1 or old_position > total:
            raise Exception("Question not found at position")
        if new_position < 1:
            new_position = 1
        if new_position > total:
            new_position = total

        if old_position == new_position:
            conn.close()
            return

        moving = ids.pop(old_position - 1)
        ids.insert(new_position - 1, moving)

        _rewrite_sequential_positions(cur, ids)
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def delete_question_by_position(position):
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM Question WHERE position = ?", (position,))
        row = cur.fetchone()
        if not row:
            raise Exception("Question not found")
        qid = row[0]
        cur.execute("DELETE FROM Answer WHERE question_id = ?", (qid,))
        cur.execute("DELETE FROM Question WHERE id = ?", (qid,))

        cur.execute("SELECT id FROM Question ORDER BY position ASC")
        ids_left = [r[0] for r in cur.fetchall()]
        _rewrite_sequential_positions(cur, ids_left)

        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def delete_question_by_id(qid):
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cur = conn.cursor()
    try:
        cur.execute("SELECT id FROM Question WHERE id = ?", (qid,))
        row = cur.fetchone()
        if not row:
            conn.close()
            return
        cur.execute("DELETE FROM Answer WHERE question_id = ?", (qid,))
        cur.execute("DELETE FROM Question WHERE id = ?", (qid,))

        cur.execute("SELECT id FROM Question ORDER BY position ASC")
        ids_left = [r[0] for r in cur.fetchall()]
        _rewrite_sequential_positions(cur, ids_left)

        conn.commit()
    finally:
        conn.close()

def delete_all_questions():
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cur = conn.cursor()
    cur.execute("DELETE FROM Answer")
    cur.execute("DELETE FROM Question")
    conn.commit()
    conn.close()

def get_questions_count(quiz_name="default"):
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cur = conn.cursor()
    quiz_id = get_quiz_id(cur, quiz_name)
    cur.execute("SELECT COUNT(*) FROM Question WHERE quiz_id = ?", (quiz_id,))
    count = cur.fetchone()[0]
    conn.close()
    return count