from flask import Flask, request, jsonify
from flask_cors import CORS
from jwt_utils import build_token, decode_token, is_token_valid
import hashlib
from question_model import Question
import sqlite3
from question_repository import (
    insert_question,
    get_question_by_id,
    get_question_by_position,
    update_question,
    move_question,
    delete_question_by_id,
    delete_all_questions,
    get_questions_count,
    delete_question_by_position
)
import init_db
import json

DB_PATH = "DB_quiz.db"

app = Flask(__name__)
CORS(app)
app.url_map.strict_slashes = False

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    size = get_questions_count()
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cur = conn.cursor()
    cur.execute("SELECT playerName, score FROM Participation ORDER BY score DESC, playerName ASC")
    scores = [{"playerName": row[0], "score": row[1]} for row in cur.fetchall()]
    conn.close()
    return {"size": size, "scores": scores}, 200

@app.route('/login', methods=['POST'])
def login():
    payload = request.get_json()
    password = payload.get('password')
    hashed_pwd = hashlib.md5(password.encode()).hexdigest()
    correct_hashed_pwd = "d278077bbfe7285a144d4b5b11adb9cf"
    if hashed_pwd == correct_hashed_pwd:
        token = build_token()
        return jsonify({"token": token})
    else:
        return 'Unauthorized', 401

def _safe_json():
    data = request.get_json(silent=True)
    if data is not None:
        return data
    if request.data:
        try:
            return json.loads(request.data.decode('utf-8'))
        except:
            return {}
    return {}

@app.route('/questions', methods=['POST'])
def post_question():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return 'Unauthorized', 401
    token = auth_header.split(" ")[1]
    if not is_token_valid(token):
        return 'Unauthorized', 401

    data = _safe_json()
    if not data:
        return jsonify({"error": "Bad request"}), 400
    try:
        question = Question.from_json(data)
    except Exception:
        return jsonify({"error": "Bad request"}), 400

    try:
        qid = insert_question(question)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"id": qid}), 200

@app.route('/questions/<int:qid>', methods=['GET'])
def get_question_by_id_route(qid):
    question = get_question_by_id(qid)
    if question:
        return jsonify(question.to_json()), 200
    return jsonify({"error": "Not found"}), 404

@app.route('/questions', methods=['GET'])
def get_question_by_position_route():
    position = request.args.get('position', type=int)
    if position is None:
        return jsonify({"error": "Missing position"}), 400
    question = get_question_by_position(position)
    if question:
        return jsonify(question.to_json()), 200
    return jsonify({"error": "Not found"}), 404

@app.route('/questions/all', methods=['GET'])
def get_all_questions():
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cur = conn.cursor()
    cur.execute("SELECT id FROM Question ORDER BY position ASC")
    question_ids = [row[0] for row in cur.fetchall()]
    conn.close()
    questions = []
    for qid in question_ids:
        question = get_question_by_id(qid)
        if question:
            questions.append(question.to_json())
    return jsonify(questions), 200

@app.route('/questions/<int:qid>', methods=['DELETE'])
def delete_question(qid):
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return 'Unauthorized', 401
        token = auth_header.split(" ")[1]
        if not is_token_valid(token):
            return 'Unauthorized', 401
        question = get_question_by_id(qid)
        if not question:
            return '', 404
        delete_question_by_id(qid)
        return '', 204
    except Exception as e:
        print("Erreur DELETE /questions/<id> :", e)
        return jsonify({"error": str(e)}), 500

@app.route('/questions/<int:qid>', methods=['PUT'])
def put_question(qid):
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith("Bearer "):
            return 'Unauthorized', 401
        token = auth_header.split(" ")[1]
        if not is_token_valid(token):
            return 'Unauthorized', 401

        existing = get_question_by_id(qid)
        if not existing:
            return '', 404

        data = _safe_json()

        if 'position' in data and isinstance(data['position'], int):
            new_pos = data['position']
            if new_pos != existing.position:
                total = get_questions_count()
                if new_pos < 1:
                    new_pos = 1
                if new_pos > total:
                    new_pos = total
                move_question(existing.position, new_pos)
                existing = get_question_by_id(qid)

        try:
            update_question(
                qid,
                title=data.get('title'),
                text=data.get('text'),
                image=data.get('image'),
                possibleAnswers=data.get('possibleAnswers')
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        return '', 204
    except Exception as e:
        print("Erreur PUT /questions/<id> :", e)
        return jsonify({"error": str(e)}), 500

@app.route('/questions/all', methods=['DELETE'])
def delete_all_questions_route():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return 'Unauthorized', 401
    token = auth_header.split(" ")[1]
    if not is_token_valid(token):
        return 'Unauthorized', 401
    delete_all_questions()
    return '', 204

@app.route('/participations/all', methods=['DELETE'])
def delete_all_participations():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return 'Unauthorized', 401
    token = auth_header.split(" ")[1]
    if not is_token_valid(token):
        return 'Unauthorized', 401
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cur = conn.cursor()
    cur.execute("DELETE FROM Participation")
    conn.commit()
    conn.close()
    return '', 204

@app.route('/rebuild-db', methods=['POST'])
def rebuild_db():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return 'Unauthorized', 401
    token = auth_header.split(" ")[1]
    if not is_token_valid(token):
        return 'Unauthorized', 401
    init_db.create_db()
    return "Ok", 200

@app.route('/participations', methods=['POST'])
def add_participation():
    data = request.get_json(silent=True)
    if not data or 'playerName' not in data or 'answers' not in data:
        return jsonify({"error": "Bad request"}), 400

    playerName = data['playerName']
    answers = data['answers']

    if not isinstance(answers, list):
        return jsonify({"error": "Bad request"}), 400

    nb_questions = get_questions_count()
    if len(answers) != nb_questions:
        return jsonify({"error": "Bad request"}), 400

    conn = sqlite3.connect(DB_PATH, timeout=5)
    cur = conn.cursor()
    cur.execute("SELECT id FROM Question ORDER BY position ASC")
    question_ids = [row[0] for row in cur.fetchall()]
    conn.close()

    score = 0
    for i, raw_answer in enumerate(answers):
        if i >= len(question_ids):
            break
        qid = question_ids[i]
        question = get_question_by_id(qid)
        if not question:
            continue
        correct_indices = [idx for idx, ans in enumerate(question.possibleAnswers) if ans['isCorrect']]
        if not correct_indices:
            continue
        selected = resolve_selected_index(raw_answer, question.possibleAnswers)
        if selected is None:
            continue
        if selected in correct_indices:
            score += 1

    conn = sqlite3.connect(DB_PATH, timeout=5)
    cur = conn.cursor()
    cur.execute("INSERT INTO Participation (playerName, score) VALUES (?, ?)", (playerName, score))
    conn.commit()
    conn.close()

    return jsonify({"playerName": playerName, "score": score}), 200

@app.route('/questions', methods=['PUT'])
def update_or_move_question_by_position():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return 'Unauthorized', 401
    token = auth_header.split(" ")[1]
    if not is_token_valid(token):
        return 'Unauthorized', 401

    data = _safe_json()
    if 'position' not in data:
        pos_arg = request.args.get('position', type=int)
        if pos_arg:
            data['position'] = pos_arg
    if 'position' not in data:
        return jsonify({"error": "position required"}), 400

    position = data['position']
    new_position = data.get('newPosition')
    title = data.get('title')
    text = data.get('text')
    image = data.get('image')
    possibleAnswers = data.get('possibleAnswers')

    q = get_question_by_position(position)
    if not q:
        return jsonify({"error": "Not found"}), 404

    try:
        if new_position is not None and new_position != position:
            total = get_questions_count()
            if new_position < 1:
                new_position = 1
            if new_position > total:
                new_position = total
            if new_position != position:
                move_question(position, new_position)
                q = get_question_by_position(new_position)

        if any(v is not None for v in [title, text, image, possibleAnswers]):
            update_question(
                q.id,
                title=title,
                text=text,
                image=image,
                possibleAnswers=possibleAnswers
            )
        return '', 204
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/questions', methods=['DELETE'])
def delete_question_by_position_route():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return 'Unauthorized', 401
    token = auth_header.split(" ")[1]
    if not is_token_valid(token):
        return 'Unauthorized', 401

    data = _safe_json()
    if 'position' not in data:
        pos_arg = request.args.get('position', type=int)
        if pos_arg:
            data['position'] = pos_arg
    if 'position' not in data:
        return jsonify({"error": "position required"}), 400
    try:
        delete_question_by_position(data['position'])
        return '', 204
    except Exception:
        return jsonify({"error": "Not found"}), 404
    
def resolve_selected_index(raw, answers_list):
    if not answers_list:
        return None
    if isinstance(raw, int):
        if 0 <= raw < len(answers_list):
            return raw
        return None
    if isinstance(raw, bool):
        return 0 if raw and len(answers_list) > 0 else None
    if isinstance(raw, str):
        val = raw.strip().lower()
        for idx, ans in enumerate(answers_list):
            if ans['text'].strip().lower() == val:
                return idx
        return None
    if isinstance(raw, dict):
        for k in ('index', 'answerIndex', 'answer'):
            if k in raw:
                return resolve_selected_index(raw[k], answers_list)
    return None

if __name__ == "__main__":
    app.run()