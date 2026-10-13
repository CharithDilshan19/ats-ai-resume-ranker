import re
import os
import json

# Comprehensive domain taxonomy for semantic skill inference
TECH_TAXONOMY = {
    'python': ['flask', 'django', 'fastapi', 'pandas', 'numpy', 'scipy', 'pytorch', 'tensorflow', 'celery', 'pydantic', 'pytest', 'sqlalchemy'],
    'java': ['spring', 'spring boot', 'hibernate', 'maven', 'gradle', 'jpa', 'jvm', 'j2ee', 'microservices'],
    'javascript': ['typescript', 'react', 'vue', 'angular', 'node', 'nodejs', 'express', 'nextjs', 'next.js', 'redux', 'svelte'],
    'typescript': ['javascript', 'react', 'angular', 'vue', 'node', 'nestjs'],
    'c++': ['c', 'stl', 'cuda', 'cmake', 'embedded', 'system programming'],
    'c#': ['.net', 'asp.net', 'unity', 'entity framework', 'csharp', 'dotnet'],
    'mysql': ['sql', 'relational database', 'database management', 'mariadb', 'rdbms', 'queries'],
    'postgresql': ['sql', 'postgres', 'relational database', 'rdbms', 'psql'],
    'mongodb': ['nosql', 'document database', 'mongoose'],
    'docker': ['kubernetes', 'k8s', 'containers', 'containerization', 'docker-compose', 'podman'],
    'kubernetes': ['docker', 'k8s', 'container orchestration', 'helm', 'cloud native'],
    'aws': ['cloud', 'ec2', 's3', 'lambda', 'cloudformation', 'iam', 'dynamodb'],
    'azure': ['cloud', 'microsoft azure', 'azure devops', 'blob storage'],
    'gcp': ['cloud', 'google cloud', 'bigquery', 'cloud run'],
    'machine learning': ['ml', 'deep learning', 'nlp', 'computer vision', 'data science', 'scikit-learn', 'tensorflow', 'pytorch'],
    'frontend': ['html', 'html5', 'css', 'css3', 'javascript', 'react', 'vue', 'tailwind', 'bootstrap'],
    'backend': ['api', 'rest api', 'microservices', 'server', 'database', 'sql', 'flask', 'django', 'express', 'spring'],
    'devops': ['ci/cd', 'docker', 'kubernetes', 'jenkins', 'github actions', 'terraform', 'ansible']
}

def extract_tokens(text):
    return set(re.findall(r'\b[a-zA-Z0-9_+#.-]+\b', text.lower()))

def token_in_text(token, text):
    escaped = re.escape(token.strip().lower())
    pattern = rf'(?<![a-zA-Z0-9]){escaped}(?![a-zA-Z0-9])'
    return bool(re.search(pattern, text, flags=re.IGNORECASE))

def detect_experience(text):
    """Detects total years of experience from resume text."""
    # Pattern 1: Explicit years e.g. "4 years of experience", "5+ yrs"
    exp_matches = re.findall(r'(\d{1,2})\+?\s*(?:years?|yrs?)(?:\s+of)?\s+experience', text, re.IGNORECASE)
    if exp_matches:
        years = max([int(y) for y in exp_matches if int(y) < 40])
        return f"{years}+ years stated"

    # Pattern 2: Date ranges e.g. "2021 - Present", "2019 - 2023"
    year_ranges = re.findall(r'\b(20[0-2]\d)\s*[-–—to]+\s*(present|current|20[0-2]\d)\b', text, re.IGNORECASE)
    if year_ranges:
        total_span = 0
        current_year = 2026
        for start, end in year_ranges:
            start_yr = int(start)
            end_yr = current_year if end.lower() in ['present', 'current'] else int(end)
            if 0 < (end_yr - start_yr) <= 15:
                total_span = max(total_span, end_yr - start_yr)
        if total_span > 0:
            return f"~{total_span} years career span"

    return "Entry level / Not specified"

def detect_education(text):
    """Detects degree / education level."""
    degrees = []
    if token_in_text('ph.d', text) or token_in_text('phd', text) or 'doctorate' in text:
        degrees.append('Ph.D')
    if token_in_text('m.tech', text) or token_in_text('ms', text) or token_in_text('master', text) or 'mca' in text:
        degrees.append("Master's Degree")
    if token_in_text('b.tech', text) or token_in_text('b.e', text) or token_in_text('bs', text) or token_in_text('bachelor', text) or 'bca' in text:
        degrees.append("Bachelor's Degree")
    if token_in_text('diploma', text):
        degrees.append("Diploma")

    return ", ".join(degrees) if degrees else "Degree not explicitly stated"

def evaluate_resume_ai(raw_text, required_skills_list, job_title=""):
    """
    Evaluates resume using semantic matching, experience analysis,
    and multi-factor ATS scoring.
    """
    text_lower = raw_text.lower()
    
    # 1. Semantic Skill Matching
    matched_direct = []
    matched_semantic = []
    missing_skills = []

    for req in required_skills_list:
        req_clean = req.strip().lower()
        if not req_clean:
            continue

        # Check direct word-boundary match
        if token_in_text(req_clean, text_lower):
            matched_direct.append(req_clean)
            continue

        # Check semantic ontology / related tools
        related_found = []
        if req_clean in TECH_TAXONOMY:
            for related in TECH_TAXONOMY[req_clean]:
                if token_in_text(related, text_lower):
                    related_found.append(related)
        
        # Check reverse ontology
        for parent_tech, children in TECH_TAXONOMY.items():
            if req_clean in children and token_in_text(parent_tech, text_lower):
                related_found.append(parent_tech)

        if related_found:
            sample_related = ", ".join(related_found[:2])
            matched_semantic.append(f"{req_clean} (via {sample_related})")
        else:
            missing_skills.append(req_clean)

    total_req = len(required_skills_list)
    if total_req > 0:
        # Full credit for direct, 75% credit for semantic inference
        skill_score = ((len(matched_direct) * 1.0) + (len(matched_semantic) * 0.75)) / total_req
        skill_score = min(1.0, skill_score) * 65 # 65% weight
    else:
        skill_score = 65

    # 2. Experience Detection & Score (20% weight)
    exp_detected = detect_experience(raw_text)
    if "+" in exp_detected or "career span" in exp_detected:
        exp_score = 20
    else:
        exp_score = 8

    # 3. Education & Structural Score (15% weight)
    edu_detected = detect_education(raw_text)
    structure_score = 0
    if "Master" in edu_detected or "Ph.D" in edu_detected:
        structure_score += 10
    elif "Bachelor" in edu_detected:
        structure_score += 8
    else:
        structure_score += 4

    # Structure checks (sections present)
    for section in ['experience', 'education', 'skills', 'projects', 'summary']:
        if section in text_lower:
            structure_score += 1
    structure_score = min(15, structure_score)

    # 4. Total Final ATS Score (0 - 100)
    final_score = int(skill_score + exp_score + structure_score)
    final_score = max(0, min(100, final_score))

    # If almost all skills are missing and it's not a resume (e.g. physics practical book)
    if total_req > 0 and len(matched_direct) == 0 and len(matched_semantic) == 0:
        final_score = min(final_score, 15)

    # 5. Recommendation Tier
    if final_score >= 75:
        recommendation = "Strong Match"
    elif final_score >= 50:
        recommendation = "Moderate Match"
    else:
        recommendation = "Low Match"

    # 6. AI Summary Generation
    all_matched = matched_direct + matched_semantic
    matched_count = len(all_matched)
    missing_count = len(missing_skills)

    summary_parts = []
    if matched_count > 0:
        sample_m = ", ".join(all_matched[:3])
        summary_parts.append(f"Demonstrates competence in {sample_m}.")
    else:
        summary_parts.append("Lacks primary required technical skills for this role.")

    summary_parts.append(f"Experience: {exp_detected}. Education: {edu_detected}.")

    if missing_count > 0:
        sample_miss = ", ".join(missing_skills[:3])
        summary_parts.append(f"Missing key requirements: {sample_miss}.")
    else:
        summary_parts.append("Meets all requested core technical criteria.")

    ai_summary = " ".join(summary_parts)

    return {
        "score": final_score,
        "matched_direct": matched_direct,
        "matched_semantic": matched_semantic,
        "all_matched": all_matched,
        "missing_skills": missing_skills,
        "recommendation": recommendation,
        "experience_detected": exp_detected,
        "education_detected": edu_detected,
        "ai_summary": ai_summary
    }
