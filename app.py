# app.py

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

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Harsha's AI Resume Matcher",
    page_icon="🧠",
    layout="wide",
)

# -------------------- HEADER --------------------
st.markdown(
    """
    <div style="padding: 10px 0 20px 0;">
        <h1 style="font-size: 40px; margin-bottom: 5px;">
            🧠 Harsha's <span style="color:#ff4b4b;">AI Resume & JD Matcher</span>
        </h1>
        <p style="font-size:16px; color:#555; max-width: 900px;">
            Paste or upload a Job Description (JD) and your Resume. 
            This tool compares skills, highlights gaps, and helps you tailor your profile for each role.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.markdown("### 👨‍💻 Built by Harsha Reddy")
    st.write(
        "Aspiring Data / AI / Cloud Engineer.\n\n"
        "This project uses Python + NLP (spaCy) to compare resumes with job descriptions."
    )

    st.markdown("#### 🔗 Links")
    st.markdown("- GitHub: [Harshareddy17](https://github.com/Harshareddy17)")
    # If you have LinkedIn, uncomment and add your link:
    # st.markdown("- LinkedIn: [Your Name](https://www.linkedin.com/in/your-link/)")

    st.markdown("#### ⚙️ How to use")
    st.markdown(
        """
        1. Paste or upload the **JD**  
        2. Paste or upload your **Resume**  
        3. Click **Analyze Match**  
        4. See match score, matched and missing skills
        """
    )

# -------------------- INPUT TABS --------------------
tab_paste, tab_upload = st.tabs(["✍️ Paste Text", "📁 Upload Files"])

with tab_paste:
    st.subheader("Paste Job Description")
    jd_text_input = st.text_area(
        "Job Description",
        height=180,
        placeholder="Paste the job description here...",
    )

    st.subheader("Paste Resume")
    resume_text_input = st.text_area(
        "Resume",
        height=220,
        placeholder="Paste your resume here...",
    )

with tab_upload:
    st.subheader("Upload Job Description File")
    jd_file = st.file_uploader(
        "Upload JD (PDF, DOCX, TXT)",
        type=["pdf", "docx", "txt"],
        key="jd_file",
    )

    st.subheader("Upload Resume File")
    resume_file = st.file_uploader(
        "Upload Resume (PDF, DOCX, TXT)",
        type=["pdf", "docx", "txt"],
        key="resume_file",
    )

st.markdown("---")
st.markdown("### 🔍 Match Analysis")

# -------------------- ANALYSIS BUTTON --------------------
if st.button("🔍 Analyze Match", type="primary"):
    jd_text = ""
    resume_text = ""

    # Priority: pasted text; if empty, use uploaded file
    if jd_text_input.strip():
        jd_text = jd_text_input
    elif jd_file is not None:
        jd_text = read_uploaded_file(jd_file)

    if resume_text_input.strip():
        resume_text = resume_text_input
    elif resume_file is not None:
        resume_text = read_uploaded_file(resume_file)

    if not jd_text or not resume_text:
        st.error(
            "Please provide both Job Description and Resume (either by pasting or uploading).")
    else:
        with st.spinner("Analyzing with NLP and skill matching..."):
            # Clean text
            jd_clean = clean_text(jd_text)
            resume_clean = clean_text(resume_text)

            # Skill extraction (hard + soft)
            jd_hard, jd_soft = extract_skills_from_text(jd_clean)
            resume_hard, resume_soft = extract_skills_from_text(resume_clean)

            jd_all_skills = jd_hard.union(jd_soft)
            resume_all_skills = resume_hard.union(resume_soft)

            # Score + matched / missing
            score, matched, missing = calculate_match_score(
                jd_all_skills, resume_all_skills)

            # Keywords
            jd_keywords = extract_keywords_nlp(jd_text)
            resume_keywords = extract_keywords_nlp(resume_text)

            # Role guess
            guessed_role = guess_role_from_jd(jd_text)

        # -------------------- SUMMARY METRICS --------------------
        col_score, col_role = st.columns([1, 2])

        with col_score:
            st.metric(label="Match Score", value=f"{score}%")

        with col_role:
            st.write(f"**Guessed Role (from JD):** `{guessed_role}`")

        # Bar chart for matched vs missing
        df_score = build_score_dataframe(matched, missing)
        st.bar_chart(df_score.set_index("Category"))

        # -------------------- SKILL DETAILS --------------------
        st.markdown("#### ✅ Skills Overview")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Matched Skills")
            if matched:
                st.write(", ".join(sorted(matched)))
            else:
                st.write("_No JD skills found in your resume._")

        with col2:
            st.subheader("Missing Skills (from JD)")
            if missing:
                st.write(", ".join(sorted(missing)))
                st.info(
                    "Consider adding projects, certifications, or bullets to cover some of these "
                    "skills if you actually have experience with them."
                )
            else:
                if jd_all_skills:
                    st.write(
                        "_You cover all detectable JD skills in your resume!_")
                else:
                    st.write(
                        "_JD does not contain enough clear skills. Try with a more detailed, technical JD._"
                    )

        # -------------------- KEYWORDS --------------------
        st.markdown("---")
        st.markdown("### 🔑 Keyword Summary (NLP-based)")

        col3, col4 = st.columns(2)

        with col3:
            st.markdown("**Top JD Keywords**")
            if jd_keywords:
                st.write(", ".join(jd_keywords))
            else:
                st.write("_No strong keywords detected in JD._")

        with col4:
            st.markdown("**Top Resume Keywords**")
            if resume_keywords:
                st.write(", ".join(resume_keywords))
            else:
                st.write("_No strong keywords detected in resume._")

        # -------------------- IMPROVEMENT TIPS --------------------
        st.markdown("---")
        st.markdown("### 💡 How You Can Improve Alignment")

        if not jd_all_skills:
            st.write(
                "- The JD is very generic or high-level. Try another JD with more explicit skill requirements.\n"
                "- This tool works best for roles that list specific technical or domain skills."
            )
        else:
            st.write(
                "- Highlight **matched skills** more clearly in your resume (Summary / Skills / Projects sections).\n"
                "- For **missing skills**, consider learning them or adding them only if you truly know them.\n"
                "- Rephrase some bullet points using the same language as the JD (without copying exact sentences)."
            )

# -------------------- FOOTER --------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#888; font-size:13px;'>"
    "Made with ❤️ in Python & Streamlit by Harsha Reddy"
    "</p>",
    unsafe_allow_html=True,
)
