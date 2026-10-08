"""
FreightIQ — Page 01: Market Overview
The primary landing dashboard for freight market intelligence.
"""

import sys, os
from pathlib import Path

# Ensure paths
_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import streamlit as st

try:
    st.set_page_config(
        page_title="Market Overview — FreightIQ",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
except Exception:
    pass

from utils.theme import inject_css
inject_css()

if not st.session_state.get("_app_runner", False):
    from components.sidebar import render_sidebar
    render_sidebar()

from utils.data_loader import (
    load_forecasts,
    load_cleaned_dataset,
    get_all_forecasts,
    get_current_bdi,
    get_forecast_date,
)
from components.header import render_hero, render_disclaimer, render_footer
from components.kpi_cards import render_kpi_cards
from components.charts import build_bdi_forecast_chart
from components.forecast_cards import render_forecast_cards
from components.insights import render_market_insight

# ── Load data ────────────────────────────────────────────────────────────────
forecast_df = load_forecasts()
cleaned_df  = load_cleaned_dataset()

current_bdi   = get_current_bdi(forecast_df)
forecast_date = get_forecast_date(forecast_df)
forecasts     = get_all_forecasts(forecast_df) if forecast_df is not None else [None, None, None]

# ── Hero ─────────────────────────────────────────────────────────────────────
render_hero(
    title="FREIGHTIQ",
    subtitle="Dry Bulk Market Intelligence & Machine Learning Forecasting",
    badge_text="MARKET OVERVIEW",
    meta_items=[
        ("Last Updated", forecast_date or "—"),
        ("Model", "XGBoost Regression"),
        ("Primary Target", "Baltic Dry Index (BDI)"),
        ("Forecast Horizons", "7 / 14 / 30 Observations"),
        ("Dataset", "3,204 rows · 33 features"),
    ],
)

# ── Error guard ───────────────────────────────────────────────────────────────
if forecast_df is None:
    st.error(
        "Forecast data not found. "
        "Expected: `data/processed/model1_final_forecasts.csv`"
    )
    st.stop()

# ── KPI Cards ─────────────────────────────────────────────────────────────────
render_kpi_cards(current_bdi, forecasts, forecast_date)

st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)

# ── Main BDI chart ────────────────────────────────────────────────────────────
st.markdown(
    "<div class='fiq-section-title'>BDI Historical Trend & Forecast</div>",
    unsafe_allow_html=True,
)
if cleaned_df is not None:
    fig = build_bdi_forecast_chart(cleaned_df, forecasts)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True})
else:
    st.warning("Historical BDI data not found. Expected: `data/processed/model1_cleaned_dataset.csv`")

# ── Forecast Summary ──────────────────────────────────────────────────────────
st.markdown(
    "<div class='fiq-section-title' style='margin-top:1.5rem;'>Forecast Summary</div>",
    unsafe_allow_html=True,
)
render_forecast_cards(forecasts)

# ── Market Insight ────────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
render_market_insight(current_bdi, forecasts)

# ── Disclaimer ────────────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:1.5rem;'></div>", unsafe_allow_html=True)
render_disclaimer()

# ── Footer ────────────────────────────────────────────────────────────────────
render_footer()
