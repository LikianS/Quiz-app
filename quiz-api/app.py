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
import log_repository
import os
import openai
import re
from dotenv import load_dotenv
load_dotenv()


OPENAI_KEY = os.environ.get('OPENAI_API_KEY')
openai.api_key = OPENAI_KEY
OPENAI_MODEL = os.environ.get('OPENAI_MODEL', 'gpt-3.5-turbo')
OPENAI_BASE_URL = os.environ.get('OPENAI_BASE_URL')  # optional; e.g. OpenRouter endpoint


DB_PATH = "DB_quiz.db"

app = Flask(__name__)
CORS(app)
app.url_map.strict_slashes = False

init_db.create_log_table()

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
        log_repository.insert_log("admin", "login", "/login", "success", f"token={token}")
        return jsonify({"token": token})
    else:
        log_repository.insert_log("admin", "login", "/login", "fail", f"password={password}")
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
        log_repository.insert_log("admin", "create_question", "/questions", "fail", "bad request json")
        return jsonify({"error": "Bad request"}), 400

    try:
        qid = insert_question(question)
    except Exception as e:
        log_repository.insert_log("admin", "create_question", "/questions", "fail", str(e))
        return jsonify({"error": str(e)}), 400
    log_repository.insert_log("admin", "create_question", "/questions", "success", f"id={qid}")
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
            log_repository.insert_log("admin", "delete_question", f"/questions/{qid}", "fail", "not found")
            return '', 404
        delete_question_by_id(qid)
        log_repository.insert_log("admin", "delete_question", f"/questions/{qid}", "success", "deleted")
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
            log_repository.insert_log("admin", "edit_question", f"/questions/{qid}", "fail", "not found")
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
            log_repository.insert_log("admin", "edit_question", f"/questions/{qid}", "fail", str(e))
            return jsonify({"error": str(e)}), 500

        log_repository.insert_log("admin", "edit_question", f"/questions/{qid}", "success", "updated")
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
    log_repository.insert_log("admin", "delete_all_questions", "/questions/all", "success", "all deleted")
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
    log_repository.insert_log("admin", "delete_all_participations", "/participations/all", "success", "all deleted")
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
    log_repository.insert_log("admin", "rebuild_db", "/rebuild-db", "success", "db rebuilt")
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

    score = data.get('score')
    if score is None:
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
    log_repository.insert_log(playerName, "add_participation", "/participations", "success", f"score={score}")
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
        log_repository.insert_log("admin", "edit_question_by_position", "/questions", "fail", f"position={position} not found")
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
        log_repository.insert_log("admin", "edit_question_by_position", "/questions", "success", f"position={position}")
        return '', 204
    except Exception as e:
        log_repository.insert_log("admin", "edit_question_by_position", "/questions", "fail", str(e))
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
        log_repository.insert_log("admin", "delete_question_by_position", "/questions", "success", f"position={data['position']}")
        return '', 204
    except Exception:
        log_repository.insert_log("admin", "delete_question_by_position", "/questions", "fail", f"position={data['position']} not found")
        return jsonify({"error": "Not found"}), 404
    
@app.route('/questions/all', methods=['GET'])
def get_all_questions():
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cur = conn.cursor()
    cur.execute("SELECT id FROM Question ORDER BY position ASC")
    rows = cur.fetchall()
    conn.close()
    questions = []
    for row in rows:
        q = get_question_by_id(row[0])
        if q:
            questions.append(q.to_json())
    return jsonify(questions),200

def resolve_selected_index(raw, answers_list):
    if not answers_list:
        return None
    if isinstance(raw, int):
        if 1 <= raw <= len(answers_list):
            return raw - 1
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


@app.route('/questions/generate', methods=['POST'])
def generate_questions_route():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return 'Unauthorized', 401
    token = auth_header.split(" ")[1]
    if not is_token_valid(token):
        return 'Unauthorized', 401

    data = _safe_json()
    text = data.get('text')
    count = int(data.get('count', 3))
    auto = bool(data.get('autoInsert', False))

    if not text:
        return jsonify({'error': 'text required'}), 400

    if not OPENAI_KEY or openai is None:
        return jsonify({'error': 'OpenAI key not configured on server'}), 500

    system_prompt = (
        "You are an assistant that receives a source text and must generate a JSON array of questions in FRENCH "
        "suitable for insertion into the quiz backend. Return ONLY valid JSON (an array) with objects having: "
        "title (string), text (string), image (string|null), possibleAnswers (array of objects with fields text:string and isCorrect:boolean). "
        "The 'title' and 'text' fields must be written in French. The 'image' field should contain either null or a short FRENCH keyword/phrase (not a URL) that best describes an image to illustrate the question (e.g. \"Tour Eiffel\", \"mitose\"). "
        "Example: [{\"title\":\"...\",\"text\":\"...\",\"image\":null,\"possibleAnswers\":[{\"text\":\"a\",\"isCorrect\":false},{\"text\":\"b\",\"isCorrect\":true}]}]. "
        "Génère exactement le nombre de questions demandé et ne renvoie aucun commentaire additionnel."
    )
    user_prompt = f"Texte source :\n\"\"\"\n{text}\n\"\"\"\n\nRetourne {count} question(s) en français au format JSON conforme au schéma décrit (title, text, image, possibleAnswers)."


    default_headers = None
    if OPENAI_BASE_URL and 'openrouter.ai' in OPENAI_BASE_URL.lower():
        hdrs = {}
        site = os.environ.get('OPENROUTER_SITE_URL')
        title = os.environ.get('OPENROUTER_APP_NAME')
        if site:
            hdrs['HTTP-Referer'] = site
        if title:
            hdrs['X-Title'] = title
        if hdrs:
            default_headers = hdrs
    client = openai.OpenAI(base_url=OPENAI_BASE_URL, default_headers=default_headers) if (OPENAI_BASE_URL or default_headers) else openai.OpenAI()
    try:
        resp = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
            ],
            temperature=0.3,
            max_tokens=1200
        )
        content = resp.choices[0].message.content
    except Exception as e:
        try:
            from openai import RateLimitError, AuthenticationError, APIConnectionError, APITimeoutError
            if isinstance(e, RateLimitError):
                return jsonify({'error': 'insufficient_quota', 'message': 'OpenAI quota exceeded or rate limited. Check your plan/billing.'}), 429
            if isinstance(e, AuthenticationError):
                return jsonify({'error': 'openai_auth_failed', 'message': 'Invalid or missing OpenAI API key.'}), 401
            if isinstance(e, (APIConnectionError, APITimeoutError)):
                return jsonify({'error': 'openai_unreachable', 'message': 'Unable to reach OpenAI API. Try again later.'}), 502
        except Exception:
            pass
        return jsonify({'error': 'openai_request_failed', 'message': str(e)}), 500


    m = re.search(r"(\[\s*\{[\s\S]*\}\s*\])", content)
    json_text = m.group(1) if m else content

    try:
        parsed = json.loads(json_text)
    except Exception as e:
        return jsonify({'error': 'Failed to parse JSON from OpenAI', 'detail': str(e), 'content': content}), 500

    if auto:
        inserted_ids = []
        for q in parsed:
            try:
                question = Question.from_json(q)
                qid = insert_question(question)
                inserted_ids.append(qid)
            except Exception as e:
                log_repository.insert_log('admin', 'generate_insert', '/questions/generate', 'fail', str(e))
        log_repository.insert_log('admin', 'generate_insert', '/questions/generate', 'success', f'count={len(inserted_ids)}')
        return jsonify({'inserted': inserted_ids}), 200

    return jsonify(parsed), 200

@app.route('/logs', methods=['GET'])
def get_logs():
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith("Bearer "):
        return 'Unauthorized', 401
    token = auth_header.split(" ")[1]
    if not is_token_valid(token):
        return 'Unauthorized', 401
    logs = log_repository.get_logs()
    return jsonify(logs), 200

if __name__ == "__main__":
    app.run()