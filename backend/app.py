from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import fitz
import os
import mysql.connector
from ai_engine import evaluate_resume_ai

app = Flask(__name__)
CORS(app)

# Ensure upload directory path is absolute and reliable regardless of run directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.abspath(os.path.join(BASE_DIR, '..', 'uploads', 'resumes'))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database Configuration (supports local defaults and cloud env variables)
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'ats_ai'),
    'port': int(os.environ.get('DB_PORT', 3306))
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

@app.route('/create-job', methods=['POST'])
def create_job():
    data = request.json or {}
    title = data.get('title', '').strip()
    skills = data.get('skills', '').strip()

    if not title:
        return jsonify({"error": "Job title is required"}), 400

    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO jobs (title, required_skills) VALUES (%s, %s)", (title, skills))
        conn.commit()
        job_id = cur.lastrowid
        return jsonify({"job_id": job_id, "message": "Job created successfully", "title": title})
    finally:
        conn.close()

@app.route('/jobs', methods=['GET'])
def get_jobs():
    conn = get_db()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT id, title, required_skills FROM jobs ORDER BY id DESC")
        jobs = cur.fetchall()
        return jsonify(jobs)
    finally:
        conn.close()

@app.route('/upload', methods=['POST'])
@app.route('/upload-resume', methods=['POST'])
def upload():
    if 'resume' not in request.files:
        return jsonify({"error": "No resume file provided"}), 400

    file = request.files['resume']
    if not file or file.filename == '':
        return jsonify({"error": "No file selected"}), 400

    job_id = request.form.get('job_id')
    try:
        job_id = int(job_id) if job_id else 1
    except ValueError:
        job_id = 1

    filename = secure_filename(file.filename)
    if not filename:
        filename = "resume.pdf"

    if not filename.lower().endswith('.pdf'):
        return jsonify({"error": "Only PDF files are currently supported"}), 400

    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    # Extract text using PyMuPDF
    try:
        doc = fitz.open(path)
        text = "".join([p.get_text() for p in doc])
        doc.close()
    except Exception as e:
        return jsonify({"error": f"Failed to parse PDF: {str(e)}"}), 400

    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute("SELECT required_skills, title FROM jobs WHERE id=%s", (job_id,))
        job = cur.fetchone()

        if not job or not job[0]:
            required = ["java", "spring", "mysql"]
            job_title = "Developer"
        else:
            required = [s.strip().lower() for s in job[0].split(',') if s.strip()]
            job_title = job[1] or ""

        # AI Semantic Evaluation
        eval_result = evaluate_resume_ai(text, required, job_title=job_title)

        score = eval_result["score"]
        matched_str = ", ".join(eval_result["all_matched"])
        missing_str = ", ".join(eval_result["missing_skills"])
        ai_summary = eval_result["ai_summary"]
        recommendation = eval_result["recommendation"]
        experience_detected = eval_result["experience_detected"]
        education_detected = eval_result["education_detected"]

        # Save to DB
        cur.execute("INSERT INTO resumes (file_name, raw_text) VALUES (%s, %s)", (filename, text))
        resume_id = cur.lastrowid

        cur.execute(
            """INSERT INTO rankings 
               (job_id, resume_id, score, matched_skills, missing_skills, ai_summary, recommendation, experience_detected, education_detected) 
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (job_id, resume_id, score, matched_str, missing_str, ai_summary, recommendation, experience_detected, education_detected)
        )
        conn.commit()

        return jsonify({
            "file": filename,
            "score": score,
            "matched": eval_result["all_matched"],
            "missing": eval_result["missing_skills"],
            "ai_summary": ai_summary,
            "recommendation": recommendation,
            "experience": experience_detected,
            "education": education_detected,
            "job_id": job_id
        })
    finally:
        conn.close()

@app.route('/rankings/<int:job_id>', methods=['GET'])
def get_rankings(job_id):
    conn = get_db()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("""
            SELECT r.file_name, rk.score, rk.matched_skills, rk.missing_skills,
                   rk.ai_summary, rk.recommendation, rk.experience_detected, rk.education_detected
            FROM rankings rk
            JOIN resumes r ON rk.resume_id = r.id
            WHERE rk.job_id = %s
            ORDER BY rk.score DESC, rk.id DESC
        """, (job_id,))
        data = cur.fetchall()
        return jsonify(data)
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)