"""
FreightIQ — Global CSS & Theme
Shared style injection used by all pages.
"""

import streamlit as st

GLOBAL_CSS = """
<style>
/* ── Base layout ── */
html, body, [data-testid="stAppViewContainer"] {
    background-color: #0B1120 !important;
    color: #F8FAFC !important;
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
}
[data-testid="stSidebar"] {
    background-color: #111827 !important;
    border-right: 1px solid #1E2940 !important;
}
[data-testid="stSidebarContent"] {
    padding: 1rem 1rem !important;
}
/* ── Sidebar nav links ── */
[data-testid="stSidebarNavLink"] {
    color: #94A3B8 !important;
    border-radius: 6px;
    margin-bottom: 2px;
}
[data-testid="stSidebarNavLink"]:hover,
[data-testid="stSidebarNavLink"][aria-selected="true"] {
    background-color: #1E293B !important;
    color: #38BDF8 !important;
}
/* ── Metric cards ── */
[data-testid="stMetric"] {
    background-color: #151E2E !important;
    border: 1px solid #1E2940 !important;
    border-radius: 10px !important;
    padding: 1rem 1.2rem !important;
}
[data-testid="stMetricLabel"] { color: #94A3B8 !important; font-size: 0.72rem !important; text-transform: uppercase; letter-spacing: 0.08em; }
[data-testid="stMetricValue"] { color: #F8FAFC !important; font-size: 1.6rem !important; font-weight: 700; }
[data-testid="stMetricDelta"] { font-size: 0.82rem !important; }
/* ── Tab styling ── */
[data-testid="stTabs"] button {
    color: #64748B !important;
    border-bottom: 2px solid transparent;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #38BDF8 !important;
    border-bottom: 2px solid #38BDF8 !important;
}
/* ── Dataframe / table ── */
[data-testid="stDataFrame"] { border-radius: 8px; overflow: hidden; }
/* ── Dividers ── */
hr { border-color: #1E2940 !important; }
/* ── Hide Streamlit branding ── */
#MainMenu, footer, header { visibility: hidden; }
/* ── Card helper class ── */
.fiq-card {
    background: #151E2E;
    border: 1px solid #1E2940;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}
.fiq-label {
    color: #64748B;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.3rem;
}
.fiq-value {
    color: #F8FAFC;
    font-size: 1.5rem;
    font-weight: 700;
}
.fiq-delta-pos { color: #22C55E; font-size: 0.85rem; font-weight: 600; }
.fiq-delta-neg { color: #EF4444; font-size: 0.85rem; font-weight: 600; }
.fiq-delta-neu { color: #F59E0B; font-size: 0.85rem; font-weight: 600; }
.fiq-section-title {
    color: #F8FAFC;
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    margin-bottom: 0.75rem;
}
.fiq-muted { color: #64748B; font-size: 0.8rem; }
.fiq-badge {
    display: inline-block;
    background: #0F2036;
    color: #38BDF8;
    border: 1px solid #38BDF8;
    border-radius: 4px;
    padding: 2px 8px;
    font-size: 0.68rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.fiq-badge-green {
    background: #052E16;
    color: #22C55E;
    border-color: #22C55E;
}
.fiq-badge-yellow {
    background: #2D1D00;
    color: #F59E0B;
    border-color: #F59E0B;
}
.fiq-insight-box {
    background: #0F1E35;
    border-left: 3px solid #38BDF8;
    border-radius: 6px;
    padding: 1rem 1.25rem;
    color: #CBD5E1;
    font-size: 0.92rem;
    line-height: 1.7;
    margin: 0.5rem 0;
}
.fiq-disclaimer {
    background: #0F1423;
    border: 1px solid #1E2940;
    border-radius: 8px;
    padding: 1rem 1.25rem;
    color: #64748B;
    font-size: 0.78rem;
    line-height: 1.6;
}
.fiq-footer {
    text-align: center;
    color: #64748B;
    font-size: 0.72rem;
    padding: 1.5rem 0 0.5rem 0;
    border-top: 1px solid #1E2940;
    margin-top: 2rem;
}
.fiq-pill {
    display: inline-block;
    background: #1E2940;
    color: #94A3B8;
    border-radius: 20px;
    padding: 3px 10px;
    font-size: 0.7rem;
    margin: 2px;
}
</style>
"""


def inject_css() -> None:
    """Inject global CSS into the current Streamlit page."""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
