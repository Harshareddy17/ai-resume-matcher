import streamlit as st
from utils import (
    read_uploaded_file,
    clean_text,
    extract_skills_from_text,
    extract_keywords_nlp,
    calculate_match_score,
    build_score_dataframe,
    guess_role_from_jd,
)

st.set_page_config(page_title="AI Resume Matcher",
                   page_icon="📄", layout="wide")

st.title("📄 AI Resume & Job Description Matcher")
st.write(
    "Upload or paste a **Job Description (JD)** and your **Resume**. "
    "This tool will show skill match %, matched/missing skills, and keywords."
)

tabs = st.tabs(["✍️ Paste Text", "📁 Upload Files"])

with tabs[0]:
    st.subheader("Paste Job Description")
    jd_text_input = st.text_area("Job Description", height=200)

    st.subheader("Paste Resume")
    resume_text_input = st.text_area("Resume", height=200)

with tabs[1]:
    st.subheader("Upload Job Description")
    jd_file = st.file_uploader("Upload JD File", type=["pdf", "docx", "txt"])

    st.subheader("Upload Resume")
    resume_file = st.file_uploader(
        "Upload Resume File", type=["pdf", "docx", "txt"])

st.markdown("---")

if st.button("🔍 Analyze Match"):
    jd_text = ""
    resume_text = ""

    if jd_text_input.strip():
        jd_text = jd_text_input
    elif jd_file:
        jd_text = read_uploaded_file(jd_file)

    if resume_text_input.strip():
        resume_text = resume_text_input
    elif resume_file:
        resume_text = read_uploaded_file(resume_file)

    if not jd_text or not resume_text:
        st.error("Please provide both Job Description and Resume.")
    else:
        with st.spinner("Analyzing..."):
            jd_clean = clean_text(jd_text)
            resume_clean = clean_text(resume_text)

            jd_tech, jd_soft = extract_skills_from_text(jd_clean)
            resume_tech, resume_soft = extract_skills_from_text(resume_clean)

            jd_skills = jd_tech.union(jd_soft)
            resume_skills = resume_tech.union(resume_soft)

            score, matched, missing = calculate_match_score(
                jd_skills, resume_skills)

            jd_keywords = extract_keywords_nlp(jd_text)
            resume_keywords = extract_keywords_nlp(resume_text)

            role = guess_role_from_jd(jd_text)

        st.success(f"Match Score: **{score}%**")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Matched Skills")
            st.write(", ".join(sorted(matched)) if matched else "No matches")

        with col2:
            st.subheader("Missing Skills")
            st.write(", ".join(sorted(missing))
                     if missing else "No missing skills")

        st.subheader("Keyword Summary (NLP Based)")
        st.write("**JD Keywords:**", ", ".join(jd_keywords))
        st.write("**Resume Keywords:**", ", ".join(resume_keywords))
