"""
PlacifyAI - Shared CSS Styling & Themes
Contains the unified design system color palette, global CSS injections,
and configured Plotly templates for the application.
"""

import streamlit as st
import plotly.graph_objects as go

# ── Design System Color Tokens ───────────────────────────────────────────────
COLORS = {
    "background": "#0f172a",       # Slate 900
    "surface": "#1e293b",          # Slate 800
    "surface_hover": "#334155",    # Slate 700
    "border": "#334155",           # Slate 700
    
    # Contextual Colors
    "primary": "#4f46e5",          # Indigo 600
    "secondary": "#06b6d4",        # Cyan 500
    "success": "#10b981",          # Emerald 500
    "warning": "#f59e0b",          # Amber 500
    "danger": "#ef4444",           # Red 500
    
    # Text Hierarchy
    "text_primary": "#f1f5f9",     # Slate 100 (Primary Headers/Values)
    "text_secondary": "#94a3b8",   # Slate 400 (Labels/Sub-headers)
    "text_muted": "#64748b",       # Slate 500 (Small footnotes/indicators)
}

def inject_global_css():
    """Inject unified premium styling into the current Streamlit page."""
    st.markdown(
        f"""
        <style>
        /* ── Import Google Font ── */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

        /* ── Global Styles ── */
        *, html, body {{
            font-family: 'Inter', sans-serif !important;
        }}
        
        .stApp {{
            background: {COLORS["background"]} !important;
            color: {COLORS["text_primary"]} !important;
        }}

        /* ── Sidebar Styling ── */
        section[data-testid="stSidebar"] {{
            background: linear-gradient(180deg, {COLORS["surface"]} 0%, {COLORS["background"]} 100%) !important;
            border-right: 1px solid {COLORS["border"]} !important;
        }}
        
        /* Make sidebar components readable */
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] h4,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p {{
            color: {COLORS["text_primary"]} !important;
        }}

        /* Custom Streamlit Navigation (st.navigation) styling */
        [data-testid="stSidebarNav"] a span {{
            color: {COLORS["text_secondary"]} !important;
            font-weight: 500 !important;
            font-size: 0.95rem !important;
        }}
        
        [data-testid="stSidebarNav"] a:hover span {{
            color: {COLORS["text_primary"]} !important;
        }}
        
        [data-testid="stSidebarNav"] a[aria-current="page"] {{
            background-color: rgba(79, 70, 229, 0.15) !important;
            border-left: 4px solid {COLORS["primary"]} !important;
            border-radius: 4px !important;
        }}
        
        [data-testid="stSidebarNav"] a[aria-current="page"] span {{
            color: {COLORS["text_primary"]} !important;
            font-weight: 700 !important;
        }}

        /* ── Streamlit Elements Overrides ── */
        [data-testid="stHeader"] {{
            background-color: {COLORS["background"]} !important;
        }}
        [data-testid="stAppDeployButton"] {{
            display: none !important;
        }}
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* ── Sidebar Toggle Buttons ── */
        button[data-testid="stBaseButton-headerNoPadding"],
        button[data-testid*="CollapseButton"] {{
            color: {COLORS["text_primary"]} !important;
            background-color: {COLORS["surface"]} !important;
            border: 1px solid {COLORS["border"]} !important;
            border-radius: 8px !important;
            padding: 6px !important;
            opacity: 1 !important;
            transition: all 0.2s ease !important;
        }}
        button[data-testid="stBaseButton-headerNoPadding"]:hover,
        button[data-testid*="CollapseButton"]:hover {{
            background-color: {COLORS["surface_hover"]} !important;
            border-color: {COLORS["primary"]} !important;
        }}
        button[data-testid="stBaseButton-headerNoPadding"] svg,
        button[data-testid*="CollapseButton"] svg {{
            color: {COLORS["text_primary"]} !important;
            fill: {COLORS["text_primary"]} !important;
        }}
        
        /* Bulletproof hiding of keyboard shortcut overlays / 'keyb' labels */
        button[data-testid="stBaseButton-headerNoPadding"] span,
        button[data-testid="stBaseButton-headerNoPadding"] div,
        button[data-testid*="CollapseButton"] span,
        button[data-testid*="CollapseButton"] div,
        [data-testid="stHeader"] button span,
        [data-testid="stHeader"] button div,
        [data-testid="stSidebar"] button span,
        [data-testid="stSidebar"] button div,
        button[data-testid="stBaseButton-headerNoPadding"] *:not(svg):not(path),
        button[data-testid*="CollapseButton"] *:not(svg):not(path) {{
            display: none !important;
            font-size: 0px !important;
            color: transparent !important;
            width: 0px !important;
            height: 0px !important;
            overflow: hidden !important;
            visibility: hidden !important;
            opacity: 0 !important;
        }}

        /* Sidebar collapse button inside the sidebar */
        [data-testid="stSidebar"] button[kind="headerNoPadding"],
        [data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"] {{
            color: {COLORS["text_primary"]} !important;
            opacity: 1 !important;
        }}
        [data-testid="stSidebar"] button[data-testid="stBaseButton-headerNoPadding"] svg {{
            color: {COLORS["text_primary"]} !important;
            stroke: {COLORS["text_primary"]} !important;
        }}

        /* ── Inputs & Labels ── */
        label, 
        .stWidgetLabel p, 
        div[data-testid="stWidgetLabel"] p,
        div[data-testid="stWidgetLabel"] label {{
            color: {COLORS["text_primary"]} !important;
            font-weight: 500 !important;
            font-size: 0.95rem !important;
        }}

        .stSelectbox > div > div,
        .stNumberInput > div > div > input {{
            background-color: {COLORS["surface"]} !important;
            border: 1px solid {COLORS["border"]} !important;
            color: {COLORS["text_primary"]} !important;
            border-radius: 8px !important;
            font-size: 0.95rem !important;
        }}

        /* Fix contrast for sliders */
        .stSlider > div > div > div {{
            color: {COLORS["text_primary"]} !important;
        }}

        /* ── Form Design ── */
        .stForm {{
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.8) 100%) !important;
            border: 1px solid {COLORS["border"]} !important;
            border-radius: 16px !important;
            padding: 24px !important;
        }}

        /* ── Primary Action Button & Form Submit Button ── */
        .stButton > button,
        div[data-testid="stFormSubmitButton"] button {{
            background: linear-gradient(135deg, {COLORS["primary"]} 0%, #6366f1 100%) !important;
            color: #ffffff !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.6rem 2rem !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 14px rgba(79, 70, 229, 0.3) !important;
            width: 100% !important;
        }}

        .stButton > button:hover,
        div[data-testid="stFormSubmitButton"] button:hover {{
            background: linear-gradient(135deg, #6366f1 0%, #818cf8 100%) !important;
            box-shadow: 0 6px 20px rgba(79, 70, 229, 0.5) !important;
            transform: translateY(-1px) !important;
        }}

        /* ── Premium Landing Cards (st.page_link) ── */
        div.stColumn [data-testid*="stPageLink"] {{
            display: block !important;
            background: linear-gradient(135deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
            border: 1px solid {COLORS["border"]} !important;
            border-radius: 16px !important;
            padding: 32px 24px !important;
            text-align: center !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
            cursor: pointer !important;
            min-height: 160px !important;
        }}

        div.stColumn [data-testid*="stPageLink"]:hover {{
            border-color: {COLORS["primary"]} !important;
            box-shadow: 0 8px 32px rgba(79, 70, 229, 0.25) !important;
            transform: translateY(-4px) !important;
        }}

        div.stColumn [data-testid*="stPageLink"] a {{
            background-color: transparent !important;
            border: none !important;
            text-decoration: none !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            gap: 12px !important;
            width: 100% !important;
            height: 100% !important;
            padding: 0 !important;
            box-shadow: none !important;
        }}

        div.stColumn [data-testid*="stPageLink"] button {{
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            width: 100% !important;
            height: 100% !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
        }}

        div.stColumn [data-testid*="stPageLink"] a span[data-testid="stPageLinkIcon"] {{
            font-size: 3rem !important;
            margin-right: 0 !important;
            margin-bottom: 8px !important;
        }}

        div.stColumn [data-testid*="stPageLink"] a span:not([data-testid="stPageLinkIcon"]) {{
            color: {COLORS["text_primary"]} !important;
            font-weight: 700 !important;
            font-size: 1.25rem !important;
            line-height: 1.4 !important;
            white-space: pre-wrap !important;
            text-align: center !important;
        }}

        /* ── Metric Cards ── */
        div[data-testid="stMetric"] {{
            background: linear-gradient(135deg, {COLORS["surface"]} 0%, {COLORS["background"]} 100%) !important;
            border: 1px solid {COLORS["border"]} !important;
            border-radius: 12px !important;
            padding: 16px 20px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3) !important;
            transition: all 0.3s ease !important;
        }}

        div[data-testid="stMetric"]:hover {{
            border-color: {COLORS["primary"]} !important;
            box-shadow: 0 4px 24px rgba(79, 70, 229, 0.2) !important;
            transform: translateY(-2px) !important;
        }}

        div[data-testid="stMetric"] label {{
            color: {COLORS["text_secondary"]} !important;
            font-size: 0.85rem !important;
            font-weight: 500 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }}

        div[data-testid="stMetric"] [data-testid="stMetricValue"] {{
            color: {COLORS["text_primary"]} !important;
            font-size: 1.8rem !important;
            font-weight: 700 !important;
        }}

        /* ── KPI Cards (Dashboard Custom HTML) ── */
        .kpi-card {{
            background: linear-gradient(135deg, {COLORS["surface"]} 0%, {COLORS["background"]} 100%);
            border: 1px solid {COLORS["border"]};
            border-radius: 16px;
            padding: 24px;
            text-align: center;
            box-shadow: 0 4px 24px rgba(0, 0, 0, 0.3);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
            height: 100%;
        }}

        .kpi-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            border-radius: 16px 16px 0 0;
        }}

        .kpi-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }}

        .kpi-card .kpi-icon {{
            font-size: 1.8rem;
            margin-bottom: 8px;
        }}

        .kpi-card .kpi-value {{
            font-size: 1.8rem;
            font-weight: 800;
            color: {COLORS["text_primary"]};
            line-height: 1.2;
            margin-bottom: 4px;
        }}

        .kpi-card .kpi-label {{
            font-size: 0.8rem;
            color: {COLORS["text_secondary"]};
            text-transform: uppercase;
            letter-spacing: 1px;
            font-weight: 600;
        }}

        /* Color modifiers for KPI cards */
        .kpi-blue::before {{ background: linear-gradient(90deg, {COLORS["primary"]}, {COLORS["secondary"]}); }}
        .kpi-green::before {{ background: linear-gradient(90deg, {COLORS["success"]}, #059669); }}
        .kpi-purple::before {{ background: linear-gradient(90deg, #a371f7, #8957e5); }}
        .kpi-pink::before {{ background: linear-gradient(90deg, #f778ba, #db61a2); }}
        .kpi-orange::before {{ background: linear-gradient(90deg, {COLORS["warning"]}, #d29922); }}
        .kpi-cyan::before {{ background: linear-gradient(90deg, #39d2c0, {COLORS["secondary"]}); }}

        .kpi-blue:hover {{ border-color: {COLORS["primary"]}; }}
        .kpi-green:hover {{ border-color: {COLORS["success"]}; }}
        .kpi-purple:hover {{ border-color: #a371f7; }}
        .kpi-pink:hover {{ border-color: #f778ba; }}
        .kpi-orange:hover {{ border-color: {COLORS["warning"]}; }}
        .kpi-cyan:hover {{ border-color: #39d2c0; }}

        /* ── Predictor Result Cards ── */
        .result-card {{
            background: linear-gradient(135deg, {COLORS["surface"]} 0%, {COLORS["background"]} 100%);
            border-radius: 16px;
            padding: 28px 24px;
            text-align: center;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            position: relative;
            overflow: hidden;
            transition: all 0.3s ease;
        }}

        .result-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.5);
        }}

        .result-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            border-radius: 16px 16px 0 0;
        }}

        .result-card .result-icon {{
            font-size: 2.2rem;
            margin-bottom: 12px;
        }}

        .result-card .result-label {{
            font-size: 0.75rem;
            color: {COLORS["text_secondary"]};
            text-transform: uppercase;
            letter-spacing: 1.5px;
            font-weight: 600;
            margin-bottom: 8px;
        }}

        .result-card .result-value {{
            font-size: 1.8rem;
            font-weight: 800;
            line-height: 1.2;
        }}

        .result-card .result-sub {{
            font-size: 0.85rem;
            color: {COLORS["text_muted"]};
            margin-top: 8px;
        }}

        .card-placed {{ border: 1px solid rgba(16, 185, 129, 0.4); }}
        .card-placed::before {{ background: linear-gradient(90deg, {COLORS["success"]}, #059669); }}
        .card-placed .result-value {{ color: {COLORS["success"]}; }}

        .card-not-placed {{ border: 1px solid rgba(239, 68, 68, 0.4); }}
        .card-not-placed::before {{ background: linear-gradient(90deg, {COLORS["danger"]}, #dc2626); }}
        .card-not-placed .result-value {{ color: {COLORS["danger"]}; }}

        .card-probability {{ border: 1px solid rgba(6, 182, 212, 0.4); }}
        .card-probability::before {{ background: linear-gradient(90deg, {COLORS["secondary"]}, #0891b2); }}
        .card-probability .result-value {{ color: {COLORS["secondary"]}; }}

        .card-company {{ border: 1px solid rgba(139, 92, 246, 0.4); }}
        .card-company::before {{ background: linear-gradient(90deg, #8b5cf6, #7c3aed); }}
        .card-company .result-value {{ color: #a78bfa; }}

        /* ── Divider ── */
        hr {{
            border-color: {COLORS["border"]} !important;
        }}

        /* ── Section Title ── */
        .section-title {{
            color: {COLORS["text_primary"]};
            font-size: 1.3rem;
            font-weight: 700;
            margin: 32px 0 16px 0;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .section-title .title-line {{
            flex: 1;
            height: 1px;
            background: linear-gradient(90deg, {COLORS["border"]}, transparent);
        }}

        /* ── Form Section Header ── */
        .form-section-title {{
            color: {COLORS["text_primary"]};
            font-size: 1rem;
            font-weight: 600;
            margin: 8px 0;
            padding: 8px 12px;
            background: rgba(79, 70, 229, 0.08);
            border-left: 3px solid {COLORS["primary"]};
            border-radius: 0 8px 8px 0;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

def get_plotly_theme(height=400):
    """Return Plotly template dict matching the design system colors."""
    return dict(
        layout=go.Layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color=COLORS["text_primary"], size=12),
            title=dict(
                font=dict(color=COLORS["text_primary"], size=13.5, family="Inter, sans-serif"),
                x=0.01,
                y=0.95
            ),
            xaxis=dict(
                gridcolor="rgba(51, 65, 85, 0.3)",
                linecolor="rgba(51, 65, 85, 0.5)",
                zerolinecolor="rgba(51, 65, 85, 0.3)",
                tickfont=dict(color=COLORS["text_secondary"]),
                title=dict(font=dict(color=COLORS["text_secondary"])),
            ),
            yaxis=dict(
                gridcolor="rgba(51, 65, 85, 0.3)",
                linecolor="rgba(51, 65, 85, 0.5)",
                zerolinecolor="rgba(51, 65, 85, 0.3)",
                tickfont=dict(color=COLORS["text_secondary"]),
                title=dict(font=dict(color=COLORS["text_secondary"])),
            ),
            legend=dict(
                bgcolor="rgba(0,0,0,0)",
                bordercolor="rgba(51, 65, 85, 0.3)",
                font=dict(color=COLORS["text_primary"]),
            ),
            margin=dict(l=40, r=40, t=56, b=40),
            height=height,
        )
    )
