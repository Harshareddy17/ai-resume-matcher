# utils.py

import re
from typing import List, Set, Tuple

import pdfplumber
from docx import Document
import spacy
import pandas as pd

from skills_config import (
    TECH_SKILLS,
    SOFT_SKILLS,
    SALES_SKILLS,
    SUPPORT_OPS_SKILLS,
    ROLE_KEYWORDS,
)

# Load spaCy model once
nlp = spacy.load("en_core_web_sm")


def read_uploaded_file(uploaded_file) -> str:
    """Reads text from uploaded file (pdf, docx, txt)."""
    if uploaded_file is None:
        return ""

    file_type = uploaded_file.type

    # Text file
    if file_type == "text/plain":
        return uploaded_file.read().decode("utf-8", errors="ignore")

    # PDF file
    if file_type == "application/pdf":
        text = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    # DOCX / DOC file
    if file_type in [
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
    ]:
        doc = Document(uploaded_file)
        return "\n".join([p.text for p in doc.paragraphs])

    # Fallback
    try:
        return uploaded_file.read().decode("utf-8", errors="ignore")
    except Exception:
        return ""


def clean_text(text: str) -> str:
    """Lowercase + remove extra spaces."""
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_skills_from_text(text: str) -> Tuple[Set[str], Set[str]]:
    """
    Extract skills by simple substring matching.

    Returns:
        hard_skills: tech + domain (sales/support/etc.)
        soft_skills: general soft skills
    """
    text_clean = clean_text(text)

    # combine all "hard" / domain skills
    hard_skill_list = list(
        set(TECH_SKILLS + SALES_SKILLS + SUPPORT_OPS_SKILLS)
    )

    hard_skills = {skill for skill in hard_skill_list if skill in text_clean}
    soft_skills = {skill for skill in SOFT_SKILLS if skill in text_clean}

    return hard_skills, soft_skills


def extract_keywords_nlp(text: str, top_n: int = 15) -> List[str]:
    """Simple keyword extraction using spaCy."""
    text = clean_text(text)
    doc = nlp(text)
    candidates: List[str] = []

    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip()
        if 1 <= len(phrase.split()) <= 4:
            candidates.append(phrase)

    for token in doc:
        if token.pos_ in {"NOUN", "PROPN"} and len(token.text) > 2:
            candidates.append(token.text)

    freq = {}
    for c in candidates:
        freq[c] = freq.get(c, 0) + 1

    sorted_keywords = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [kw for kw, _ in sorted_keywords[:top_n]]


def calculate_match_score(
    jd_skills: Set[str], resume_skills: Set[str]
) -> Tuple[float, Set[str], Set[str]]:
    """
    Score = (matched JD skills) / (total JD skills) * 100

    If the JD has very few detectable skills (< 3),
    we treat it as "not enough info" and return 0%,
    with all JD skills marked as missing.
    """
    if not jd_skills:
        return 0.0, set(), set()

    # avoid fake 100% when JD has only 1–2 skills
    if len(jd_skills) < 3:
        return 0.0, set(), jd_skills

    matched = jd_skills.intersection(resume_skills)
    missing = jd_skills.difference(resume_skills)

    score = (len(matched) / len(jd_skills)) * 100
    return round(score, 2), matched, missing


def build_score_dataframe(matched: Set[str], missing: Set[str]) -> pd.DataFrame:
    """Make a bar-chart-friendly DataFrame."""
    return pd.DataFrame(
        {
            "Category": ["Matched Skills", "Missing Skills"],
            "Count": [len(matched), len(missing)],
        }
    )


def guess_role_from_jd(jd_text: str) -> str:
    """Guess role based on JD keywords."""
    jd = clean_text(jd_text)
    scores = {}

    for role, skills in ROLE_KEYWORDS.items():
        scores[role] = sum(1 for skill in skills if skill in jd)

    best_role = max(scores, key=scores.get)
    return best_role if scores[best_role] > 0 else "general"
