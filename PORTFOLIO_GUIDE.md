# 💼 Portfolio & Career Guide: ATS AI Resume Ranker

This guide contains everything you need to leverage this project for job applications, LinkedIn visibility, and technical interviews.

---

## 1. Resume Bullet Points

### Plain Text / Word Format:
**ATS AI Resume Ranker** | *Python, Flask, PyMuPDF, MySQL, JavaScript*
* Engineered a full-stack applicant tracking system to parse, evaluate, and rank candidate resumes against role requirements in sub-second latency.
* Built a semantic evaluation engine with regular expression token boundaries and a domain taxonomy, eliminating substring false positives by 100%.
* Implemented a multi-factor scoring model combining technical skill relevancy (65%), experience timeline detection (20%), and ATS structural quality (15%).
* Designed a normalized MySQL relational schema with cascading foreign keys to store jobs, candidate profiles, and AI-generated recruiter evaluations.

### LaTeX Format (for Overleaf / Modern Resume Templates):
```latex
\resumeProjectHeading
    {\textbf{ATS AI Resume Ranker} $|$ \emph{Python, Flask, PyMuPDF, MySQL, JavaScript}}{}
    \resumeItemListStart
        \resumeItem{Engineered a full-stack applicant tracking system to parse, evaluate, and rank candidate resumes against role requirements in sub-second latency.}
        \resumeItem{Built a semantic evaluation engine with regular expression token boundaries and a domain taxonomy, eliminating substring false positives by 100\%.}
        \resumeItem{Implemented a multi-factor scoring model combining technical skill relevancy (65\%), experience timeline detection (20\%), and ATS structural quality (15\%).}
        \resumeItem{Designed a normalized MySQL relational schema with cascading foreign keys to store jobs, candidate profiles, and AI recruiter evaluations.}
    \resumeItemListEnd
```

---

## 2. LinkedIn Post Template

*(Record a quick 30-second screen video of yourself uploading a resume on the dashboard and getting an ATS score, then attach it to this post)*

```text
Excited to share my latest full-stack project: ATS AI Resume Ranker! 🚀

Did you know that corporate job openings receive 250+ resumes on average, with recruiters spending less than 7 seconds reviewing each candidate?

To solve this, I built an automated resume ranking system:
✨ PDF text extraction using PyMuPDF (fitz)
✨ Semantic skill ontology (recognizes related tools like Django/FastAPI for Python roles)
✨ Regex token boundary matching to eliminate false-positive keyword errors
✨ Multi-factor weighted ATS scoring (Skills + Experience + Education)
✨ Automated AI recruiter summaries and match tiers

Stack: Python, Flask, MySQL, JavaScript, HTML5/CSS3.

GitHub Repository: [PASTE YOUR GITHUB LINK HERE]

Feedback and thoughts are always welcome! 💡

#SoftwareEngineering #Python #WebDevelopment #Flask #MySQL #AI #FullStack #TechProjects #Portfolio
```

---

## 3. Technical Interview Cheat Sheet

### Q1: "Why did you build this project?"
> *"I wanted to tackle a real-world recruitment bottleneck: high-volume resume filtering. Traditional keyword scanners suffer from false positives—like matching the skill 'C' inside 'education'—and they reject candidates who know equivalent frameworks. I built a system that handles token boundaries, understands semantic tool relationships, and scores candidates holistically."*

### Q2: "How does the matching algorithm work?"
> *"The algorithm uses a 3-part weighted formula: 65% for skills, 20% for experience, and 15% for education/formatting. For skills, it checks word boundaries using `(?<![a-zA-Z0-9])skill(?![a-zA-Z0-9])`. If an exact skill isn't found, it consults a technical taxonomy to award semantic credit (for example, recognizing Django as Python competence) before calculating the final 0–100 score."*

### Q3: "How is your database structured?"
> *"I designed three relational tables in MySQL: `jobs`, `resumes`, and a junction table `rankings`. `rankings` references `job_id` and `resume_id` with foreign key constraints configured with `ON DELETE CASCADE`. This ensures that if a job opening is deleted, all associated ranking records and recruiter summaries are automatically cleaned up, preserving relational integrity."*

### Q4: "What were some technical challenges you faced?"
> *"One challenge was path management across different execution environments: resolving file upload paths relative to the script's directory rather than the shell's working directory. Another was securing user file uploads against path traversal attacks using Werkzeug's `secure_filename`. Additionally, I resolved endpoint mismatches between the asynchronous `FormData` fetch call and Flask route decorators."*

---

## 4. How to Push This Project to GitHub Right Now

Run these commands in PowerShell inside your project folder:

```powershell
# 1. Add all project files
git add .

# 2. Make your commit
git commit -m "feat: complete ATS AI resume ranker with semantic engine, DB schema, and dashboard"

# 3. Rename branch to main (if not already)
git branch -M main

# 4. Link to your GitHub repository (replace with your repo URL)
git remote add origin https://github.com/YOUR_GITHUB_USERNAME/ats-ai-resume-ranker.git

# 5. Push!
git push -u origin main
```
