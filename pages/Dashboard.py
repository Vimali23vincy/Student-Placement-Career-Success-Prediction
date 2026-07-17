"""
PlacifyAI – Executive Analytics Dashboard
========================================
Interactive analytics dashboard showing student placement trends, academic indicators,
and skill breakdown metrics.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
import os

# Add project root and src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from src.preprocessing import load_data
from src.styles import inject_global_css, get_plotly_theme, COLORS

# Apply global styling
inject_global_css()

# ── Load Data ──────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return load_data()

df = get_data()

# ── Sidebar Filters ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔍 Filters")

    # Add a reset button to restore default selections
    if st.button("🔄 Reset Filters", use_container_width=True):
        st.session_state.filter_branch = sorted(df["branch"].unique().tolist())
        st.session_state.filter_tier = sorted(df["college_tier"].unique().tolist())
        st.session_state.filter_status = sorted(df["placement_status"].unique().tolist())

    # Branch filter
    all_branches = sorted(df["branch"].unique().tolist())
    selected_branches = st.multiselect(
        "Branch",
        options=all_branches,
        default=all_branches,
        key="filter_branch",
    )

    # College tier filter
    all_tiers = sorted(df["college_tier"].unique().tolist())
    selected_tiers = st.multiselect(
        "College Tier",
        options=all_tiers,
        default=all_tiers,
        key="filter_tier",
    )

    # Placement status filter
    all_statuses = sorted(df["placement_status"].unique().tolist())
    selected_statuses = st.multiselect(
        "Placement Status",
        options=all_statuses,
        default=all_statuses,
        key="filter_status",
    )

    st.markdown("---")

# ── Apply Filters ──────────────────────────────────────────────────────────────
filtered_df = df[
    (df["branch"].isin(selected_branches))
    & (df["college_tier"].isin(selected_tiers))
    & (df["placement_status"].isin(selected_statuses))
].copy()

# ── Page Header & Data Bounds Indicator ────────────────────────────────────────
total_count = len(filtered_df)
grand_total = len(df)
st.markdown(
    f"""
    <div style="padding: 8px 0 0 0;">
        <h1 style="
            font-size: 2rem;
            font-weight: 800;
            background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 4px;
        ">📊 Placement Analytics Dashboard</h1>
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <p style="color: #94a3b8; font-size: 0.95rem; margin: 0;">
                Real-time insights into student placement trends, academic performance, and skill analytics.
            </p>
            <span style="
                background-color: rgba(79, 70, 229, 0.15);
                border: 1px solid rgba(79, 70, 229, 0.3);
                color: #f1f5f9;
                font-size: 0.8rem;
                padding: 4px 12px;
                border-radius: 12px;
                font-weight: 600;
            ">
                Showing {total_count:,} of {grand_total:,} Students
            </span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# ── KPI Calculations ──────────────────────────────────────────────────────────
placed_count = len(filtered_df[filtered_df["placement_status"] == "Placed"])
placement_rate = (placed_count / total_count * 100) if total_count > 0 else 0

placed_df = filtered_df[filtered_df["placement_status"] == "Placed"]
product_count = len(placed_df[placed_df["company_type"] == "Product Based"])
service_count = len(placed_df[placed_df["company_type"] == "Service Based"])
product_pct = (product_count / placed_count * 100) if placed_count > 0 else 0
service_pct = (service_count / placed_count * 100) if placed_count > 0 else 0

avg_cgpa = filtered_df["cgpa"].mean() if total_count > 0 else 0
avg_resume = filtered_df["resume_score"].mean() if total_count > 0 else 0

# ── KPI Cards Grid (Fixed Wrapping - 2 Rows of 3 Columns) ──────────────────────
def kpi_card(icon, value, label, color_class):
    return f"""
    <div class="kpi-card {color_class}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
    </div>
    """

row1_col1, row1_col2, row1_col3 = st.columns(3)
with row1_col1:
    st.markdown(kpi_card("👨‍🎓", f"{total_count:,}", "Total Students", "kpi-blue"), unsafe_allow_html=True)
with row1_col2:
    st.markdown(kpi_card("📈", f"{placement_rate:.1f}%", "Placement Rate", "kpi-green"), unsafe_allow_html=True)
with row1_col3:
    st.markdown(kpi_card("📚", f"{avg_cgpa:.2f}", "Average CGPA", "kpi-orange"), unsafe_allow_html=True)

st.markdown("<div style='margin-top: 16px;'></div>", unsafe_allow_html=True)

row2_col1, row2_col2, row2_col3 = st.columns(3)
with row2_col1:
    st.markdown(kpi_card("🏢", f"{product_pct:.1f}%", "Product Based (%)", "kpi-purple"), unsafe_allow_html=True)
with row2_col1:
    # Quick fix if user needs visual space, but wait st.columns handles spacing
    pass
with row2_col2:
    st.markdown(kpi_card("💼", f"{service_pct:.1f}%", "Service Based (%)", "kpi-pink"), unsafe_allow_html=True)
with row2_col3:
    st.markdown(kpi_card("📄", f"{avg_resume:.1f}", "Avg Resume Score", "kpi-cyan"), unsafe_allow_html=True)

# Helper to apply template styles
def style_fig(fig, height=400):
    fig.update_layout(get_plotly_theme(height)["layout"])
    return fig

# ══════════════════════════════════════════════════════════════════════════════
#  CHARTS
# ══════════════════════════════════════════════════════════════════════════════

st.markdown(
    '<div class="section-title">📊 Placement Overview <span class="title-line"></span></div>',
    unsafe_allow_html=True,
)

# ── Row 1: Placement Distribution + Placement Rate by Branch ──────────────────
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # Donut Chart for Placement Distribution
    status_counts = filtered_df["placement_status"].value_counts().reset_index()
    status_counts.columns = ["Status", "Count"]

    fig1 = go.Figure(
        data=[
            go.Pie(
                labels=status_counts["Status"],
                values=status_counts["Count"],
                hole=0.65,
                marker=dict(
                    colors=[COLORS["success"], COLORS["danger"]],
                    line=dict(color=COLORS["background"], width=2),
                ),
                textinfo="label+percent",
                textfont=dict(color=COLORS["text_primary"], size=13),
                hovertemplate="<b>%{label}</b><br>Count: %{value:,}<br>Share: %{percent}<extra></extra>",
            )
        ]
    )
    fig1.update_layout(
        title=dict(text="Overall Placement Split"),
        showlegend=True,
        annotations=[
            dict(
                text=f"<b>{placed_count:,}</b><br><span style='font-size:11px;color:#94a3b8'>Placed</span>",
                x=0.5, y=0.5, font=dict(size=20, color=COLORS["text_primary"]), showarrow=False,
            )
        ],
    )
    st.plotly_chart(style_fig(fig1, 420), use_container_width=True)

with chart_col2:
    # Placement Rate (%) by Branch to prevent absolute count scale distortion
    branch_stats = filtered_df.groupby("branch").agg(
        total=("placement_status", "count"),
        placed=("placement_status", lambda x: (x == "Placed").sum())
    ).reset_index()
    branch_stats["Placement Rate (%)"] = ((branch_stats["placed"] / branch_stats["total"]) * 100).round(1)
    branch_stats = branch_stats.sort_values("Placement Rate (%)", ascending=False)

    fig2 = px.bar(
        branch_stats,
        x="branch",
        y="Placement Rate (%)",
        text=branch_stats["Placement Rate (%)"].apply(lambda x: f"{x}%"),
        labels={"branch": "Academic Branch", "Placement Rate (%)": "Placement Success Rate (%)"},
    )
    fig2.update_traces(
        marker_color=COLORS["primary"],
        textposition="outside",
        hovertemplate="<b>%{x}</b><br>Placement Rate: %{y}%<extra></extra>",
        marker_cornerradius=6,
    )
    fig2.update_layout(
        title=dict(text="Placement Success Rate by Branch"),
        yaxis_range=[0, 110]
    )
    st.plotly_chart(style_fig(fig2, 420), use_container_width=True)


# ── Row 2: Placement by College Tier + CGPA vs Placement ──────────────────────
st.markdown(
    '<div class="section-title">🎓 Academic Analysis <span class="title-line"></span></div>',
    unsafe_allow_html=True,
)

chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    # Stacked bar chart: Placement status distribution across college tiers
    tier_data = (
        filtered_df.groupby(["college_tier", "placement_status"])
        .size()
        .reset_index(name="count")
    )
    tier_data["college_tier"] = "Tier " + tier_data["college_tier"].astype(str)

    fig3 = px.bar(
        tier_data,
        x="college_tier",
        y="count",
        color="placement_status",
        barmode="stack",
        color_discrete_map={"Placed": COLORS["success"], "Not Placed": COLORS["danger"]},
        labels={"college_tier": "College Tier", "count": "Number of Students", "placement_status": "Status"},
    )
    fig3.update_layout(title=dict(text="Placement Breakdown by College Tier"))
    fig3.update_traces(marker_line_width=0, marker_cornerradius=4)
    st.plotly_chart(style_fig(fig3, 420), use_container_width=True)

with chart_col4:
    # Box plot: CGPA distribution for Placed vs Not Placed
    fig4 = px.box(
        filtered_df,
        x="placement_status",
        y="cgpa",
        color="placement_status",
        color_discrete_map={"Placed": COLORS["success"], "Not Placed": COLORS["danger"]},
        labels={"placement_status": "Placement Status", "cgpa": "CGPA Score"},
        points="outliers",
    )
    fig4.update_layout(title=dict(text="CGPA Distributions by Placement Outcome"), showlegend=False)
    fig4.update_traces(marker=dict(opacity=0.5), line=dict(width=1.5))
    st.plotly_chart(style_fig(fig4, 420), use_container_width=True)


# ── Row 3: Internship Impact + DSA Problems ──────────────────────────────────
st.markdown(
    '<div class="section-title">💡 Skills & Experience Impact <span class="title-line"></span></div>',
    unsafe_allow_html=True,
)

chart_col5, chart_col6 = st.columns(2)

with chart_col5:
    # Bar line combination chart for internship counts impact
    intern_total = filtered_df.groupby("internships_completed").size().reset_index(name="total")
    intern_placed = (
        filtered_df[filtered_df["placement_status"] == "Placed"]
        .groupby("internships_completed")
        .size()
        .reset_index(name="placed")
    )
    intern_rate = intern_total.merge(intern_placed, on="internships_completed", how="left")
    intern_rate["placed"] = intern_rate["placed"].fillna(0)
    intern_rate["rate"] = (intern_rate["placed"] / intern_rate["total"] * 100).round(1)

    fig5 = go.Figure()
    fig5.add_trace(
        go.Bar(
            x=intern_rate["internships_completed"],
            y=intern_rate["total"],
            name="Student Volume",
            marker_color=COLORS["secondary"],
            marker_cornerradius=4,
            opacity=0.3,
            hovertemplate="Internships: %{x}<br>Count: %{y:,}<extra></extra>",
        )
    )
    fig5.add_trace(
        go.Scatter(
            x=intern_rate["internships_completed"],
            y=intern_rate["rate"],
            name="Placement Rate %",
            yaxis="y2",
            line=dict(color=COLORS["success"], width=3),
            marker=dict(size=8, color=COLORS["success"]),
            hovertemplate="Internships: %{x}<br>Rate: %{y:.1f}%<extra></extra>",
        )
    )
    fig5.update_layout(
        title=dict(text="Internships Volume & Success Rates"),
        xaxis_title="Internships Completed",
        yaxis=dict(title="Student Volume"),
        yaxis2=dict(title="Placement Rate %", overlaying="y", side="right", range=[0, 105]),
        legend=dict(x=0.01, y=0.99),
    )
    st.plotly_chart(style_fig(fig5, 420), use_container_width=True)

with chart_col6:
    # Violin plot: DSA problems solved vs Placement status
    fig6 = px.violin(
        filtered_df,
        x="placement_status",
        y="DSA_problems_solved",
        color="placement_status",
        color_discrete_map={"Placed": COLORS["success"], "Not Placed": COLORS["danger"]},
        box=True,
        labels={"placement_status": "Status", "DSA_problems_solved": "DSA Problems Solved"},
    )
    fig6.update_layout(title=dict(text="DSA Problem Solving Distribution"), showlegend=False)
    fig6.update_traces(meanline_visible=True)
    st.plotly_chart(style_fig(fig6, 420), use_container_width=True)


# ── Row 4: Resume Score Distribution ──────────────────────────────────────────
st.markdown(
    '<div class="section-title">📄 Resume Analysis <span class="title-line"></span></div>',
    unsafe_allow_html=True,
)

fig7 = px.histogram(
    filtered_df,
    x="resume_score",
    color="placement_status",
    color_discrete_map={"Placed": COLORS["success"], "Not Placed": COLORS["danger"]},
    nbins=30,
    barmode="overlay",
    opacity=0.75,
    labels={"resume_score": "Resume Evaluation Score", "placement_status": "Status"},
    marginal="box",
)
fig7.update_layout(title=dict(text="Resume Score Distribution & Density"))
fig7.update_traces(marker_line_width=0)
st.plotly_chart(style_fig(fig7, 450), use_container_width=True)



