import os
import sqlite3
import urllib3
from datetime import timedelta
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from functools import wraps

# Local Imports [cite: 1]
from config import Config
from core.processor import FileProcessor
from core.ai_engine import AIEngine

# Disable SSL warnings for corporate proxy environments (HPE) [cite: 1]
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
app.config.from_object(Config)

# Secure key handling via environment variables [cite: 1]
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "campus_bot_sih_2025")

# --- SESSION CONFIGURATION ---
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # [cite: 1]
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)  # [cite: 1]

# --- ADMIN CREDENTIALS ---
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"  # [cite: 1]


# --- AUTH DECORATOR ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash("Session expired or unauthorized access. Please login.")  # [cite: 1]
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated_function


def init_db():
    """Initializes the SQLite database for knowledge and logs."""
    with sqlite3.connect(Config.DATABASE) as conn:
        conn.execute(
            'CREATE TABLE IF NOT EXISTS knowledge (id INTEGER PRIMARY KEY, content TEXT, filename TEXT)')  # [cite: 1]
        conn.execute('''CREATE TABLE IF NOT EXISTS logs 
                       (id INTEGER PRIMARY KEY, query TEXT, answer TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')  # [cite: 1]


# --- ROUTES ---

@app.route('/')
def index():
    return render_template('chat.html')  # [cite: 1]


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pw = request.form.get('password')
        if user == ADMIN_USERNAME and pw == ADMIN_PASSWORD:
            session.permanent = True  # [cite: 1]
            session['logged_in'] = True
            return redirect(url_for('admin'))
        flash("Invalid credentials!")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()  # [cite: 1]
    return redirect(url_for('index'))


@app.route('/admin')
@login_required
def admin():
    """Dashboard to manage knowledge base files."""
    with sqlite3.connect(Config.DATABASE) as conn:
        files = conn.execute('SELECT DISTINCT filename FROM knowledge').fetchall()  # [cite: 1]
    return render_template('admin.html', files=files)


@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file selected"})  # [cite: 1]

    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No filename provided"})

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)  # [cite: 1]

    try:
        # Process file using our Multi-Modal FileProcessor (PDF/Vision)
        extracted_text = FileProcessor().process(file_path)  # [cite: 1]

        if extracted_text and len(extracted_text.strip()) > 10:
            with sqlite3.connect(Config.DATABASE) as conn:
                conn.execute('INSERT INTO knowledge (content, filename) VALUES (?, ?)',
                             (extracted_text, file.filename))  # [cite: 1]
            return jsonify({"status": "success", "message": f"Sync Complete: {file.filename} is now live."})

        # Clean up the physical file if extraction fails
        if os.path.exists(file_path):
            os.remove(file_path)  # [cite: 1]
        return jsonify({"status": "error", "message": "Extraction failed: No readable text found."})

    except Exception as e:
        return jsonify({"status": "error", "message": f"System Error: {str(e)}"})


@app.route('/delete_file', methods=['POST'])
@login_required
def delete_file():
    """Removes a specific file's knowledge from the AI database."""
    filename = request.json.get('filename')  #
    try:
        with sqlite3.connect(Config.DATABASE) as conn:
            conn.execute('DELETE FROM knowledge WHERE filename = ?', (filename,))  #
        return jsonify({"status": "success", "message": f"{filename} removed from Knowledge Base."})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/clear_chat', methods=['POST'])
def clear_chat():
    """Wipes the conversation history for the current student session."""
    session.pop('chat_history', None)  #
    return jsonify({"status": "success", "message": "Chat history cleared."})


@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    query = data.get('message')
    selected_lang = data.get('language', 'English')  # [cite: 1]

    if 'chat_history' not in session:
        session['chat_history'] = []

    history_text = "\n".join(session['chat_history'][-3:])  # [cite: 1]

    with sqlite3.connect(Config.DATABASE) as conn:
        rows = conn.execute('SELECT content FROM knowledge').fetchall()
        context = " ".join([row[0] for row in rows])  # [cite: 1]

        if not context:
            return jsonify({"answer": "My knowledge base is empty. Please ask the admin to upload documents."})

        answer = AIEngine().get_answer(query, context, history_text, selected_lang)  # [cite: 1]
        conn.execute('INSERT INTO logs (query, answer) VALUES (?, ?)', (query, answer))

    session['chat_history'].append(f"Student: {query}")
    session['chat_history'].append(f"Assistant: {answer}")
    session.modified = True  # [cite: 1]

    return jsonify({"answer": answer})


@app.route('/logs')
@login_required
def view_logs():
    with sqlite3.connect(Config.DATABASE) as conn:
        logs = conn.execute('SELECT * FROM logs ORDER BY timestamp DESC LIMIT 100').fetchall()  # [cite: 1]
    return render_template('logs.html', logs=logs)


if __name__ == '__main__':
    init_db()  # [cite: 1]
    app.run(debug=True, host='0.0.0.0', port=5000)