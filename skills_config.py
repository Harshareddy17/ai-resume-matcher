# skills_config.py

# ---------- Core technical skills ----------
TECH_SKILLS = [
    "python", "java", "c++", "c", "javascript", "html", "css",
    "sql", "mysql", "postgresql", "mongodb",
    "pandas", "numpy", "matplotlib", "seaborn",
    "machine learning", "deep learning", "data analysis",
    "data science", "power bi", "tableau", "excel",
    "git", "github", "docker", "kubernetes",
    "aws", "azure", "gcp",
    "rest api", "flask", "django", "fastapi",
]

# ---------- General soft skills ----------
SOFT_SKILLS = [
    "communication", "teamwork", "problem solving",
    "leadership", "time management", "critical thinking",
    "adaptability", "self motivated", "collaboration",
    "customer service",  # very common
]

# ---------- Sales / Retail skills ----------
SALES_SKILLS = [
    "sales",
    "retail",
    "customer service",
    "cash handling",
    "cashier",
    "inventory management",
    "stocking",
    "product knowledge",
    "upselling",
    "cross selling",
    "pos",
    "point of sale",
    "store operations",
    "merchandising",
    "greeting customers",
]

# ---------- Support Ops / IT operations skills ----------
SUPPORT_OPS_SKILLS = [
    "ticketing system",
    "incident management",
    "sla",
    "service level agreement",
    "root cause analysis",
    "monitoring",
    "on call",
    "shift operations",
    "troubleshooting",
    "log analysis",
    "alerting",
]


# ---------- Role-specific keyword hints ----------
ROLE_KEYWORDS = {
    "data analyst": [
        "sql", "excel", "power bi", "tableau", "pandas",
        "data cleaning", "data visualization", "reporting",
    ],
    "ml engineer": [
        "python", "machine learning", "deep learning",
        "scikit-learn", "tensorflow", "pytorch", "data preprocessing",
    ],
    "cloud engineer": [
        "aws", "azure", "gcp", "docker", "kubernetes", "ci/cd",
    ],
    "sales associate": SALES_SKILLS,
    "support ops": SUPPORT_OPS_SKILLS,
}
