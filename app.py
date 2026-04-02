import os
import sqlite3
import urllib3
from datetime import timedelta
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from functools import wraps

# Local Imports
from config import Config
from core.processor import FileProcessor
from core.ai_engine import AIEngine

# Disable SSL warnings for corporate proxy environments
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

app = Flask(__name__)
app.config.from_object(Config)

# Secure key handling
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "campus_bot_sih_2025")

# --- SESSION TIMEOUT CONFIGURATION ---
# Sets the session to expire after 30 minutes of inactivity
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Ensure upload directory exists
os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)

# --- ADMIN CREDENTIALS ---
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "password123"


# --- AUTH DECORATOR ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash("Session expired or unauthorized access. Please login.")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def init_db():
    """Initializes the SQLite database for knowledge and logs."""
    with sqlite3.connect(Config.DATABASE) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS knowledge (id INTEGER PRIMARY KEY, content TEXT, filename TEXT)')
        conn.execute('''CREATE TABLE IF NOT EXISTS logs 
                       (id INTEGER PRIMARY KEY, query TEXT, answer TEXT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')


# --- ROUTES ---

@app.route('/')
def index():
    return render_template('chat.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pw = request.form.get('password')

        if user == ADMIN_USERNAME and pw == ADMIN_PASSWORD:
            # Mark session as permanent to enable the timeout lifetime
            session.permanent = True
            session['logged_in'] = True
            return redirect(url_for('admin'))
        else:
            flash("Invalid credentials!")
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/admin')
@login_required
def admin():
    """Dashboard for management/dept to manage files."""
    with sqlite3.connect(Config.DATABASE) as conn:
        files = conn.execute('SELECT DISTINCT filename FROM knowledge').fetchall()
    return render_template('admin.html', files=files)


@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file selected"})

    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No filename provided"})

    file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(file_path)

    try:
        extracted_text = FileProcessor().process(file_path)
        if extracted_text.strip():
            with sqlite3.connect(Config.DATABASE) as conn:
                conn.execute('INSERT INTO knowledge (content, filename) VALUES (?, ?)', (extracted_text, file.filename))
            return jsonify({"status": "success", "message": f"Sync Complete: {file.filename} is now searchable."})
        return jsonify({"status": "error", "message": "Extraction failed: No readable text."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"System Error: {str(e)}"})


@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    query = data.get('message')
    selected_lang = data.get('language', 'English')

    if 'chat_history' not in session:
        session['chat_history'] = []

    history_text = "\n".join(session['chat_history'][-3:])

    with sqlite3.connect(Config.DATABASE) as conn:
        rows = conn.execute('SELECT content FROM knowledge').fetchall()
        context = " ".join([row[0] for row in rows])

        if not context:
            return jsonify({"answer": "Knowledge base empty. Please upload documents via Admin."})

        answer = AIEngine().get_answer(query, context, history_text, selected_lang)
        conn.execute('INSERT INTO logs (query, answer) VALUES (?, ?)', (query, answer))

    session['chat_history'].append(f"Student: {query}")
    session['chat_history'].append(f"Assistant: {answer}")
    session.modified = True

    return jsonify({"answer": answer})


@app.route('/logs')
@login_required
def view_logs():
    with sqlite3.connect(Config.DATABASE) as conn:
        logs = conn.execute('SELECT * FROM logs ORDER BY timestamp DESC LIMIT 100').fetchall()
    return render_template('logs.html', logs=logs)


if __name__ == '__main__':
    init_db()
    # Host on 0.0.0.0 for office network access
    app.run(debug=True, host='0.0.0.0', port=5000)