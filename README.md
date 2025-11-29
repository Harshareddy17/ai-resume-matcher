📄 AI Resume & Job Description Matcher

An intelligent NLP-powered web application that analyzes a Resume and Job Description (JD) and generates:

✔ Skill Match Percentage

✔ Matched Skills

✔ Missing Skills

✔ Resume Improvement Suggestions

✔ Summary Keywords

🚀 Live App:🚀 Live App: https://ai-resume-matcher-harshareddy17.streamlit.app

📦 GitHub Repo: https://github.com/Harshareddy17/ai-resume-matcher

✨ Features

Upload or paste Resume (PDF/TXT/DOCX)

Upload or paste Job Description

AI-based extraction using spaCy NLP

Skill matching based on a predefined skill config

Match score calculation

Highlights matched vs missing skills

Clean and modern Streamlit UI

🛠 Tech Stack

Backend: Python
Libraries:

spaCy

pdfplumber

python-docx

Streamlit

re / text processing

sklearn (optional)

Deployment: Streamlit Cloud

📁 Project Structure
├── app.py
├── utils.py
├── skills_config.py
├── requirements.txt
├── sample_jd.txt
├── sample_resume.txt
├── README.md
└── .gitignore

▶️ How to Run Locally
git clone https://github.com/Harshareddy17/ai-resume-matcher.git
cd ai-resume-matcher

# create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows

# install dependencies
pip install -r requirements.txt

# run the app
streamlit run app.py

🚀 Deployment

The app is deployed on Streamlit Cloud.

🙌 Author

Harsha Reddy

GitHub: https://github.com/Harshareddy17