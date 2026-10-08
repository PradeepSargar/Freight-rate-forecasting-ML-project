"""
FreightIQ — Intelligent Freight Market Forecasting System
Main entrypoint for the multi-page Streamlit application.
"""

import sys, os
from pathlib import Path

# Ensure application root directory is in sys.path
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

import streamlit as st

# ── Global Streamlit Page Configuration ──────────────────────────────────────
st.set_page_config(
    page_title="FreightIQ — Freight Market Forecasting",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": (
            "FreightIQ — Intelligent Freight Market Forecasting System\n"
            "Powered by XGBoost Regression\n"
            "© 2026 FreightIQ"
        ),
    },
)

from utils.theme import inject_css
inject_css()

# ── Forecast Horizon Session State Initialization ────────────────────────────
if "forecast_horizon" not in st.session_state:
    st.session_state["forecast_horizon"] = 7
st.session_state["selected_horizon"] = f"{st.session_state['forecast_horizon']} observations"

# ── Sidebar Brand ────────────────────────────────────────────────────────────
from components.sidebar import render_sidebar_top, render_sidebar_bottom
render_sidebar_top()

# ── Streamlit Navigation ─────────────────────────────────────────────────────
pages = [
    st.Page("pages/01_Market_Overview.py", title="Market Overview", icon="📊", default=True),
    st.Page("pages/02_Freight_Forecast.py", title="Freight Forecast", icon="📈"),
    st.Page("pages/03_Market_Drivers.py", title="Market Drivers", icon="📉"),
    st.Page("pages/04_Model_Performance.py", title="Model Performance", icon="🎯"),
    st.Page("pages/05_Methodology.py", title="Methodology", icon="📋"),
]

pg = st.navigation(pages)

# ── Sidebar Status & Info ────────────────────────────────────────────────────
render_sidebar_bottom()

# Set indicator flag so pages know they run within app.py router
st.session_state["_app_runner"] = True

# ── Run Selected Page ────────────────────────────────────────────────────────
pg.run()
