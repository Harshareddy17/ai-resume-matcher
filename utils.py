# utils.py

import re
from typing import List, Set, Tuple

import pdfplumber
from docx import Document
import spacy
import pandas as pd

from skills_config import TECH_SKILLS, SOFT_SKILLS, ROLE_KEYWORDS

# Load spaCy model once
nlp = spacy.load("en_core_web_sm")


def read_uploaded_file(uploaded_file) -> str:
    if uploaded_file is None:
        return ""

    file_type = uploaded_file.type

    if file_type == "text/plain":
        return uploaded_file.read().decode("utf-8", errors="ignore")

    if file_type == "application/pdf":
        text = ""
        with pdfplumber.open(uploaded_file) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    if file_type in [
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
    ]:
        doc = Document(uploaded_file)
        return "\n".join([p.text for p in doc.paragraphs])

    try:
        return uploaded_file.read().decode("utf-8", errors="ignore")
    except Exception:
        return ""


def clean_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_skills_from_text(text: str) -> Tuple[Set[str], Set[str]]:
    text_clean = clean_text(text)
    found_tech = {skill for skill in TECH_SKILLS if skill in text_clean}
    found_soft = {skill for skill in SOFT_SKILLS if skill in text_clean}
    return found_tech, found_soft


def extract_keywords_nlp(text: str, top_n: int = 15) -> List[str]:
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
    if not jd_skills:
        return 0.0, set(), set()

    matched = jd_skills.intersection(resume_skills)
    missing = jd_skills.difference(resume_skills)

    score = (len(matched) / len(jd_skills)) * 100
    return round(score, 2), matched, missing


def build_score_dataframe(matched: Set[str], missing: Set[str]) -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Category": ["Matched Skills", "Missing Skills"],
            "Count": [len(matched), len(missing)],
        }
    )


def guess_role_from_jd(jd_text: str) -> str:
    jd = clean_text(jd_text)
    scores = {}

    for role, skills in ROLE_KEYWORDS.items():
        scores[role] = sum(1 for skill in skills if skill in jd)

    best_role = max(scores, key=scores.get)
    return best_role if scores[best_role] > 0 else "general"
