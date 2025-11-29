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
    page_icon="🤖",
    layout="wide",
)

# -------------------- DARK AI BACKGROUND + GLASS UI --------------------
dark_ai_css = """
<style>
/* FULL DARK AI BACKGROUND */
[data-testid="stAppViewContainer"] {
    background-image: url("https://images.unsplash.com/photo-1504639725590-34d0984388bd?auto=format&fit=crop&w=1650&q=80");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

/* Remove default header background */
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}

/* GLASS EFFECT MAIN CONTAINER */
.block-container {
    background: rgba(0, 0, 0, 0.55);
    padding: 35px 45px;
    border-radius: 18px;
    backdrop-filter: blur(9px);
    -webkit-backdrop-filter: blur(9px);
    box-shadow: 0 10px 30px rgba(0,0,0,0.50);
    color: #ffffff;
}

/* SIDEBAR WRAPPER */
[data-testid="stSidebar"] {
    background: rgba(0,0,0,0);  /* transparent behind glass panel */
}

/* SIDEBAR GLASS PANEL */
[data-testid="stSidebar"] > div:first-child {
    background: rgba(0, 0, 0, 0.75);
    backdrop-filter: blur(6px);
    -webkit-backdrop-filter: blur(6px);
    border-radius: 12px;
    border-right: 1px solid rgba(255,255,255,0.2);
}

/* FORCE ALL SIDEBAR TEXT TO WHITE */
[data-testid="stSidebar"] * {
    color: #f5f5f5 !important;
}

/* GENERAL TEXT COLOR (CENTER) */
h1, h2, h3, h4, h5, h6, p, label, span, div, body {
    color: #e6e6e6;
}

/* METRIC VALUE STYLE */
[data-testid="stMetricValue"] {
    font-size: 30px;
    color: #76ff03 !important; /* neon green */
}
</style>
"""
st.markdown(dark_ai_css, unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown(
    """
    <div style="padding: 10px 0 20px 0;">
        <h1 style="font-size: 42px; margin-bottom: 5px; color:#76ff03;">
            🤖 Harsha's <span style="color:#00e5ff;">AI Resume & JD Matcher</span>
        </h1>
        <p style="font-size:17px; color:#cccccc; max-width: 900px;">
            AI-powered smart scanner that compares your Resume & Job Description using NLP and skills matching.
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
        "This project uses **spaCy NLP**, advanced skill matching, and Streamlit UI."
    )

    st.markdown("#### 🔗 Links")
    st.markdown("- GitHub: [Harshareddy17](https://github.com/Harshareddy17)")

    st.markdown("#### ⚙️ How to use")
    st.markdown(
        """
        1. Paste or upload JD  
        2. Paste or upload Resume  
        3. Click **Analyze**  
        4. See match score + insights  
        """
    )

# -------------------- INPUT TABS --------------------
tab_paste, tab_upload = st.tabs(["✍️ Paste Text", "📁 Upload Files"])

with tab_paste:
    st.subheader("Paste Job Description")
    jd_text_input = st.text_area(
        "Job Description",
        height=180,
        placeholder="Paste JD here...",
    )

    st.subheader("Paste Resume")
    resume_text_input = st.text_area(
        "Resume",
        height=220,
        placeholder="Paste resume here...",
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
        with st.spinner("Analyzing with AI..."):
            jd_clean = clean_text(jd_text)
            resume_clean = clean_text(resume_text)

            jd_hard, jd_soft = extract_skills_from_text(jd_clean)
            resume_hard, resume_soft = extract_skills_from_text(resume_clean)

            jd_all = jd_hard.union(jd_soft)
            res_all = resume_hard.union(resume_soft)

            score, matched, missing = calculate_match_score(jd_all, res_all)

            jd_keywords = extract_keywords_nlp(jd_text)
            resume_keywords = extract_keywords_nlp(resume_text)

            guessed_role = guess_role_from_jd(jd_text)

        # METRICS
        col_score, col_role = st.columns([1, 2])
        with col_score:
            st.metric("Match Score", f"{score}%")
        with col_role:
            st.write(f"**AI-Predicted Role:** `{guessed_role}`")

        # BAR CHART
        df_score = build_score_dataframe(matched, missing)
        st.bar_chart(df_score.set_index("Category"))

        # SKILL DETAILS
        st.markdown("#### ✅ Skills Overview")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Matched Skills")
            st.write(", ".join(sorted(matched)) if matched else "_None_")

        with col2:
            st.subheader("Missing Skills")
            st.write(", ".join(sorted(missing)) if missing else "_None_")

        # KEYWORDS
        st.markdown("---")
        st.markdown("### 🔑 NLP Keyword Summary")

        col3, col4 = st.columns(2)
        with col3:
            st.write("**JD Keywords:**")
            st.write(", ".join(jd_keywords))
        with col4:
            st.write("**Resume Keywords:**")
            st.write(", ".join(resume_keywords))

        # TIPS
        st.markdown("---")
        st.markdown("### 💡 Suggestions")
        st.write(
            "- Strengthen important keywords in your resume.\n"
            "- Add missing skills only if you genuinely have them.\n"
            "- Rewrite bullet points to better match JD wording."
        )

# -------------------- FOOTER --------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#aaa; font-size:13px;'>"
    "Made with ⚡ by <b>Harsha Reddy</b>"
    "</p>",
    unsafe_allow_html=True,
)
