"""
PlacifyAI – AI-Powered Placement Prediction Platform
=====================================================
Main application entry point.
Bootstrap routing, theme initialization, and navigation configurations.
"""

import streamlit as st
import sys
import os
import base64

# Add project root and src to path
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.styles import inject_global_css, COLORS

def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception:
        return ""

def show_home():
    """Render the main landing page content."""
    # ── Landing Hero ─────────────────────────────────────────────────────────
    logo_base64 = get_image_base64("assets/logo.png")
    logo_html = f'<img src="data:image/png;base64,{logo_base64}" width="180" style="border-radius: 16px; box-shadow: 0px 8px 30px rgba(6, 182, 212, 0.5); margin-bottom: 24px; border: 2px solid #06b6d4;"/>' if logo_base64 else '<div style="font-size: 4.5rem; margin-bottom: 16px;">🤖</div>'
    
    st.markdown(
        f"""
        <div style="text-align: center; padding: 50px 20px 20px 20px;">
            <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 16px;">
                {logo_html}
            </div>
            <h1 style="
                font-size: 3.5rem;
                font-weight: 800;
                background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
                margin-bottom: 16px;
                line-height: 1.2;
            ">PlacifyAI</h1>
            <p style="
                font-size: 1.25rem;
                color: #94a3b8;
                max-width: 650px;
                margin: 0 auto 40px auto;
                line-height: 1.6;
            ">
                AI-Powered Campus Placement Intelligence Platform.<br>
                Predict student placement status and company types with machine learning models.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Interactive Navigation Cards ─────────────────────────────────────────
    _, col_dash, col_pred, _ = st.columns([1, 2, 2, 1])

    with col_dash:
        st.page_link(
            dashboard_page,
            label="Dashboard\nAnalytics & Placement Insights",
            icon=None
        )

    with col_pred:
        st.page_link(
            predictor_page,
            label="Predictor\nML-Powered Profile Predictions",
            icon=None
        )

    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("---")

    # ── Navigation Instructions ──────────────────────────────────────────────
    st.markdown(
        """
        <div style="text-align: center; color: #64748b; padding: 10px;">
            <p style="font-size: 0.95rem;">
                👈 Use the <strong style="color: #4f46e5;">sidebar menu</strong> or select a card above to begin your journey.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Page Registration & Configuration ────────────────────────────────────────
home_page = st.Page(show_home, title="Home", icon="🤖", default=True)
dashboard_page = st.Page("pages/Dashboard.py", title="Dashboard", icon="📊")
predictor_page = st.Page("pages/Predictor.py", title="Predictor", icon="🔮")

# Configure routing table
pg = st.navigation([home_page, dashboard_page, predictor_page])

st.set_page_config(
    page_title="PlacifyAI – Placement Intelligence",
    page_icon="assets/logo.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject global styles and themes
inject_global_css()

# Render Sidebar header branding
with st.sidebar:
    logo_base64 = get_image_base64("assets/logo.png")
    if logo_base64:
        st.markdown(
            f"""
            <div style="text-align: center; padding: 10px 0 8px 0;">
                <img src="data:image/png;base64,{logo_base64}" width="140" style="border-radius: 12px; box-shadow: 0px 4px 15px rgba(6, 182, 212, 0.4); margin-bottom: 12px; border: 2px solid #06b6d4;"/>
                <h2 style="
                    font-size: 1.4rem;
                    font-weight: 800;
                    background: linear-gradient(135deg, #4f46e5, #06b6d4);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    margin: 8px 0 4px 0;
                ">PlacifyAI</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div style="text-align: center; padding: 16px 0 8px 0;">
                <span style="font-size: 2.2rem;">🤖</span>
                <h2 style="
                    font-size: 1.4rem;
                    font-weight: 800;
                    background: linear-gradient(135deg, #4f46e5, #06b6d4);
                    -webkit-background-clip: text;
                    -webkit-text-fill-color: transparent;
                    background-clip: text;
                    margin: 8px 0 4px 0;
                ">PlacifyAI</h2>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("---")

# Execute navigation router
pg.run()
