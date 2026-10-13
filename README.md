# 🚀 ATS AI Resume Ranker

> An intelligent, full-stack Applicant Tracking System (ATS) that parses, evaluates, and ranks hundreds of candidate resumes against job specifications in seconds using semantic skill inference, experience extraction, and multi-factor weighted scoring.

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=for-the-badge&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![PyMuPDF](https://img.shields.io/badge/PyMuPDF-1.28-red?style=for-the-badge)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

---

## 📌 Problem & Overview
Recruiters and hiring managers receive an average of 250+ resumes per corporate job opening and spend under 7 seconds reviewing each candidate. Conventional keyword-search filters suffer from severe **false-positive errors** (e.g., matching the letter `"C"` inside the word *"education"* or `"Java"` inside *"JavaScript"*) and fail to recognize related technologies.

**ATS AI Resume Ranker** solves this by:
1. **Preventing False Positives**: Uses strict regex token boundaries `(?<![a-zA-Z0-9])skill(?![a-zA-Z0-9])`.
2. **Semantic Knowledge Taxonomy**: Recognizes related tools (e.g., granting credit for Python if a candidate lists Django/FastAPI, or SQL if they list MySQL/PostgreSQL).
3. **Multi-Factor Weighted Scoring**: Evaluates skills (65%), experience timeline (20%), and degree/formatting structure (15%).
4. **AI Recruiter Summaries**: Automatically synthesizes candidate strengths, missing requirements, and match tiers (`Strong Match`, `Moderate Match`, `Low Match`).

---

## 🏗️ System Architecture

```
┌─────────────────────────────────┐
│     Client (dashboard.html)     │
│  - Job Selection & Creation     │
│  - PDF File Picker (FormData)   │
│  - Dynamic Leaderboard Table    │
└────────────────┬────────────────┘
                 │ HTTP REST (JSON / Multipart)
                 ▼
┌─────────────────────────────────┐
│       Flask Backend (app.py)    │
│  - Endpoints: /upload-resume,   │
│    /create-job, /rankings, /jobs│
│  - Secure File Ingestion        │
└───────┬─────────────────┬───────┘
        │                 │
        ▼                 ▼
┌──────────────┐   ┌──────────────────────────────┐
│   PyMuPDF    │   │  Semantic AI Engine          │
│ Text Stream  │   │  (ai_engine.py)              │
│  Extraction  │──>│  - Technical Domain Taxonomy │
└──────────────┘   │  - Experience & Degree Regex │
                   │  - Weighted ATS Formula      │
                   │  - Executive Recruiter Notes │
                   └──────────────┬───────────────┘
                                  │
                                  ▼
                   ┌──────────────────────────────┐
                   │    MySQL Relational DB       │
                   │  - jobs, resumes, rankings   │
                   │  - Cascading Foreign Keys    │
                   └──────────────────────────────┘
```

---

## ✨ Features
* ⚡ **High-Speed Document Parsing**: Extracts full textual representations from multi-page PDFs using PyMuPDF.
* 🧠 **Semantic Skill Inference**: Awards partial credit for relevant frameworks even if exact parent keywords are omitted.
* 📊 **Multi-Factor Scoring Model**:
  $$\text{ATS Score} = (65\% \times \text{Skills}) + (20\% \times \text{Experience}) + (15\% \times \text{Education \& Structure})$$
* 🎯 **Match Tiers**: Instant color-coded badges:
  - 🟢 **Strong Match** ($\ge 75\%$)
  - 🟡 **Moderate Match** ($50\% - 74\%$)
  - 🔴 **Low Match** ($< 50\%$)
* 🗄️ **Relational Integrity**: Foreign key constraints with `ON DELETE CASCADE` prevent database record desynchronization.
* 🌐 **Cloud & Docker Ready**: Supports `.env` configuration and standard WSGI servers (`gunicorn`).

---

## 🚀 Quick Start Guide

### 1. Prerequisites
* Python 3.10+
* MySQL Server (e.g., via XAMPP, Docker, or local service)

### 2. Clone & Install
```bash
git clone https://github.com/your-username/ats-ai-resume-ranker.git
cd ats-ai-resume-ranker
pip install -r requirements.txt
```

### 3. Initialize Database
Execute [`database.sql`](database.sql) in your MySQL environment:
```sql
CREATE DATABASE IF NOT EXISTS ats_ai;
USE ats_ai;
-- Run schema definitions from database.sql
```

### 4. Run the Application
Start the Flask server:
```bash
python backend/app.py
```
*Server starts on `http://localhost:5000`.*

### 5. Open the Dashboard
Open [`frontend/dashboard.html`](frontend/dashboard.html) directly in any modern web browser.

---

## 🧪 Testing with Sample Resumes
Sample pre-built resumes are included in the [`test_resumes/`](test_resumes/) folder:
1. **`john_doe_backend.pdf`**: Backend engineer profile (Python, Flask, MySQL, Docker, 4+ yrs experience) $\rightarrow$ **92% Strong Match**.
2. **`sarah_connor_frontend.pdf`**: Frontend developer profile (React, CSS, HTML) $\rightarrow$ **Low Match** for backend jobs.

---

## 📡 API Reference

| Endpoint | Method | Payload / Params | Description |
| :--- | :--- | :--- | :--- |
| `/jobs` | `GET` | None | Returns list of all created job openings |
| `/create-job` | `POST` | `{"title": "...", "skills": "..."}` | Creates a new job with target competencies |
| `/upload-resume` | `POST` | `multipart/form-data`: `resume`, `job_id` | Parses PDF, evaluates candidate, persists ranking |
| `/rankings/<job_id>` | `GET` | `job_id` (integer) | Returns leaderboard of candidates sorted by score |

---

## 📄 License
This project is licensed under the MIT License - feel free to use and adapt it for learning or commercial applications.