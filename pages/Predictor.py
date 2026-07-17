"""
PlacifyAI – Student Placement Predictor
========================================
Interactive student profile prediction form using trained machine learning models
to predict placement status and company type, with personalized action recommendations.
"""

import streamlit as st
import pandas as pd
import sys
import os

# Add project root and src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from src.prediction import predict_student
from src.preprocessing import load_data
from src.styles import inject_global_css, COLORS

# Apply global styling
inject_global_css()

# ── Load branch options from data ─────────────────────────────────────────────
@st.cache_data
def get_branches():
    df = load_data()
    return sorted(df["branch"].unique().tolist())

branches = get_branches()



# ── Page Header ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style="padding: 8px 0 0 0;">
        <h1 style="
            font-size: 2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #a371f7 0%, #f778ba 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 4px;
        ">🔮 Student Placement Predictor</h1>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-bottom: 24px;">
            Configure the academic, technical, and soft skill attributes below to run our dual-step prediction pipeline.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Prediction Form ───────────────────────────────────────────────────────────
with st.form("prediction_form", clear_on_submit=False):

    # ── Section: Academic Profile ──
    st.markdown('<div class="form-section-title">🎓 Academic Profile</div>', unsafe_allow_html=True)
    ac1, ac2, ac3, ac4 = st.columns(4)
    with ac1:
        college_tier = st.selectbox(
            "College Tier", 
            options=[1, 2, 3], 
            index=0,
            key="college_tier",
            help="Select the institutional ranking tier of the college."
        )
    with ac2:
        branch = st.selectbox(
            "Branch", 
            options=branches, 
            index=0,
            key="branch",
            help="Select the academic specialization branch."
        )
    with ac3:
        cgpa = st.number_input(
            "CGPA", 
            min_value=4.0, 
            max_value=10.0, 
            value=7.50, 
            step=0.1, 
            format="%.2f",
            key="cgpa",
            help="Enter CGPA score (Range: 4.0 - 10.0)."
        )
    with ac4:
        backlog = st.number_input(
            "Backlog History", 
            min_value=0, 
            max_value=5, 
            value=0, 
            step=1,
            key="backlog",
            help="Total number of historical/active backlogs (Range: 0 - 5)."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Section: Technical Skills ──
    st.markdown('<div class="form-section-title">💻 Technical Skills</div>', unsafe_allow_html=True)
    tc1, tc2, tc3 = st.columns(3)
    with tc1:
        dsa = st.number_input(
            "DSA Problems Solved", 
            min_value=0, 
            max_value=600, 
            value=200, 
            step=10,
            key="dsa",
            help="Total coding problems solved on platforms like LeetCode/HackerRank (Dataset max: 503)."
        )
    with tc2:
        github = st.number_input(
            "GitHub Repositories", 
            min_value=0, 
            max_value=25, 
            value=5, 
            step=1,
            key="github",
            help="Total public code repositories hosted on GitHub (Dataset max: 11)."
        )
    with tc3:
        hackathons = st.number_input(
            "Hackathons Participated", 
            min_value=0, 
            max_value=10, 
            value=2, 
            step=1,
            key="hackathons",
            help="Total hackathon competitions participated in (Dataset max: 5)."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Section: Experience & Soft Skills ──
    st.markdown('<div class="form-section-title">🌟 Experience & Soft Skills</div>', unsafe_allow_html=True)
    ex1, ex2, ex3, ex4 = st.columns(4)
    with ex1:
        internships = st.number_input(
            "Internships Completed", 
            min_value=0, 
            max_value=5, 
            value=1, 
            step=1,
            key="internships",
            help="Total completed professional internships (Dataset max: 3)."
        )
    with ex2:
        resume_score = st.slider(
            "Resume Score", 
            min_value=0, 
            max_value=100, 
            value=75, 
            step=1,
            key="resume_score",
            help="ATS optimization score based on resume evaluation."
        )
    with ex3:
        communication = st.slider(
            "Communication Skills", 
            min_value=0, 
            max_value=100, 
            value=70, 
            step=1,
            key="communication",
            help="Self-assessed soft skills and interview clarity score."
        )
    with ex4:
        aptitude = st.slider(
            "Aptitude Score", 
            min_value=0, 
            max_value=100, 
            value=65, 
            step=1,
            key="aptitude",
            help="Score in technical, analytical, and quantitative aptitude tests."
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # Submit button using container width stretch
    submitted = st.form_submit_button("🔮  Predict Placement", use_container_width=True)

# ── Prediction Results ────────────────────────────────────────────────────────
if submitted:
    # Validate models exist
    models_dir = os.path.join(os.path.dirname(__file__), "..", "models")
    if not os.path.exists(os.path.join(models_dir, "placement_model.pkl")):
        st.error(
            "⚠️ Models not found! Please run `python src/training.py` from the project root to train models first."
        )
        st.stop()

    # Prepare student data
    student_data = {
        "college_tier": college_tier,
        "branch": branch,
        "degree": "B.Tech",
        "cgpa": cgpa,
        "backlog_history": backlog,
        "DSA_problems_solved": dsa,
        "GitHub_repos": github,
        "internships_completed": internships,
        "resume_score": resume_score,
        "communication_skills": communication,
        "aptitude_score": aptitude,
        "hackathons_participated": hackathons,
    }

    # Run prediction
    with st.spinner("🧠 Running ML prediction..."):
        result = predict_student(student_data, models_dir=models_dir)

    st.markdown("<br>", unsafe_allow_html=True)

    is_placed = result["placement_status"] == "Placed"

    # ── Results Header ──
    st.markdown(
        f"""
        <div style="text-align: center; padding: 16px 0 8px 0;">
            <div style="
                display: inline-block;
                background: {'rgba(16, 185, 129, 0.1)' if is_placed else 'rgba(239, 68, 68, 0.1)'};
                border: 1px solid {'rgba(16, 185, 129, 0.3)' if is_placed else 'rgba(239, 68, 68, 0.3)'};
                border-radius: 24px;
                padding: 6px 20px;
                font-size: 0.85rem;
                color: {'#10b981' if is_placed else '#ef4444'};
                font-weight: 600;
                letter-spacing: 0.5px;
            ">
                {'✅ PREDICTION COMPLETE' if is_placed else '❌ PREDICTION COMPLETE'}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Result Cards ──
    r1, r2, r3 = st.columns(3)

    with r1:
        card_class = "card-placed" if is_placed else "card-not-placed"
        icon = "✅" if is_placed else "❌"
        st.markdown(
            f"""
            <div class="result-card {card_class}">
                <div class="result-icon">{icon}</div>
                <div class="result-label">Placement Status</div>
                <div class="result-value">{result['placement_status']}</div>
                <div class="result-sub">ML Model Prediction</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with r2:
        prob = result["placement_probability"]
        st.markdown(
            f"""
            <div class="result-card card-probability">
                <div class="result-icon">📊</div>
                <div class="result-label">Placement Probability</div>
                <div class="result-value">{prob}%</div>
                <div class="result-sub">Confidence Score</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with r3:
        company = result["company_type"]
        confidence = result["company_confidence"]
        company_icon = "🏢" if company == "Product Based" else ("💼" if company == "Service Based" else "➖")
        sub_text = f"Confidence Score: {confidence}%" if confidence is not None else "Not applicable"
        st.markdown(
            f"""
            <div class="result-card card-company">
                <div class="result-icon">{company_icon}</div>
                <div class="result-label">Predicted Company Type</div>
                <div class="result-value">{company}</div>
                <div class="result-sub">{sub_text}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Progress bar visualization ──
    color_start = COLORS["danger"] if prob < 30 else (COLORS["warning"] if prob < 60 else COLORS["success"])
    color_end = "#b91c1c" if prob < 30 else ("#d97706" if prob < 60 else "#047857")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        f"""
        <div style="
            background: rgba(30, 41, 59, 0.8);
            border: 1px solid #334155;
            border-radius: 12px;
            padding: 20px 24px;
        ">
            <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                <span style="color: #94a3b8; font-size: 0.85rem; font-weight: 500;">Placement Likelihood Range</span>
                <span style="color: {'#10b981' if prob >= 50 else '#ef4444'}; font-size: 0.85rem; font-weight: 700;">{prob}%</span>
            </div>
            <div style="
                background: rgba(51, 65, 85, 0.4);
                border-radius: 8px;
                height: 10px;
                overflow: hidden;
            ">
                <div style="
                    width: {prob}%;
                    height: 100%;
                    background: linear-gradient(90deg, {color_start}, {color_end});
                    border-radius: 8px;
                    transition: width 1s ease;
                "></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


