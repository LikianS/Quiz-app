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
    delete_question_by_id,
    delete_all_questions,
    get_questions_count
)
import init_db

DB_PATH = "DB_quiz.db"

app = Flask(__name__)
CORS(app)

@app.route('/')
def hello_world():
    return "Hello, saucisse"

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

@app.route('/questions', methods=['POST'])
def post_question():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return 'Unauthorized', 401
    token = auth_header.split(" ")[1]
    if not is_token_valid(token):
        return 'Unauthorized', 401
    data = request.get_json()
    question = Question.from_json(data)
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
        question = get_question_by_id(qid)
        if not question:
            return '', 404
        data = request.get_json()
        updated_question = Question.from_json(data)
        updated_question.id = qid
        try:
            update_question(updated_question)
        except Exception as e:
            if "Position already used" in str(e):
                return jsonify({"error": str(e)}), 400
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
    data = request.get_json()
    if not data or 'playerName' not in data or 'answers' not in data:
        return jsonify({"error": "Bad request"}), 400

    playerName = data['playerName']
    answers = data['answers']

    nb_questions = get_questions_count()
    if len(answers) != nb_questions:
        return jsonify({"error": "Bad request"}), 400

    conn = sqlite3.connect(DB_PATH, timeout=5)
    cur = conn.cursor()
    cur.execute("SELECT id FROM Question ORDER BY position ASC")
    question_ids = [row[0] for row in cur.fetchall()]
    conn.close()

    score = 0
    for i, answer_index in enumerate(answers):
        question = get_question_by_id(question_ids[i])
        if not question:
            continue
        possible_answers = question.possibleAnswers
        correct_index = next((idx for idx, ans in enumerate(possible_answers) if ans['isCorrect']), None)
        if correct_index is not None and answer_index == correct_index:
            score += 1

    conn = sqlite3.connect(DB_PATH, timeout=5)
    cur = conn.cursor()
    cur.execute("INSERT INTO Participation (playerName, score) VALUES (?, ?)", (playerName, score))
    conn.commit()
    conn.close()

    return jsonify({"playerName": playerName, "score": score}), 200

if __name__ == "__main__":
    app.run()