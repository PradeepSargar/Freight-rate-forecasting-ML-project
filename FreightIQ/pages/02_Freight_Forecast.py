"""
FreightIQ — Page 02: Freight Forecast Engine
Dedicated forecasting page with horizon selector, interactive charts, and summary table.
"""

import sys, os
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import streamlit as st

try:
    st.set_page_config(
        page_title="Freight Forecast — FreightIQ",
        page_icon="📈",
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
    get_forecast_for_horizon,
)
from components.header import render_hero, render_disclaimer, render_footer
from components.charts import build_horizon_chart, build_bdi_forecast_chart
from components.forecast_cards import render_forecast_table
from utils.formatting import fmt_number, fmt_pct, fmt_change, direction_arrow, direction_color

# ── Load data ────────────────────────────────────────────────────────────────
forecast_df = load_forecasts()
cleaned_df  = load_cleaned_dataset()

current_bdi   = get_current_bdi(forecast_df)
forecast_date = get_forecast_date(forecast_df)
forecasts     = get_all_forecasts(forecast_df) if forecast_df is not None else [None, None, None]
selected_horizon = st.session_state.get("selected_horizon", "7 observations")

# ── Hero ─────────────────────────────────────────────────────────────────────
render_hero(
    title="Freight Forecast Engine",
    subtitle="Machine-learning forecasts generated from historical freight-market and economic indicators.",
    badge_text="FORECAST ENGINE",
    meta_items=[
        ("Model", "XGBoost Regression"),
        ("Last Updated", forecast_date or "—"),
        ("Current BDI", fmt_number(current_bdi, 0) if current_bdi else "—"),
    ],
)

if forecast_df is None:
    st.error("Forecast data not found. Expected: `data/processed/model1_final_forecasts.csv`")
    st.stop()

# ── Horizon selector ──────────────────────────────────────────────────────────
st.markdown("<div class='fiq-section-title'>Select Forecast Horizon</div>", unsafe_allow_html=True)
col_h1, col_h2, col_h3, _ = st.columns([1, 1, 1, 3])

if col_h1.button(
    "7 Observations",
    use_container_width=True,
    type="primary" if selected_horizon == "7 observations" else "secondary",
):
    st.session_state["selected_horizon"] = "7 observations"
    st.session_state["sidebar_horizon_radio"] = "7 observations"
    st.rerun()

if col_h2.button(
    "14 Observations",
    use_container_width=True,
    type="primary" if selected_horizon == "14 observations" else "secondary",
):
    st.session_state["selected_horizon"] = "14 observations"
    st.session_state["sidebar_horizon_radio"] = "14 observations"
    st.rerun()

if col_h3.button(
    "30 Observations",
    use_container_width=True,
    type="primary" if selected_horizon == "30 observations" else "secondary",
):
    st.session_state["selected_horizon"] = "30 observations"
    st.session_state["sidebar_horizon_radio"] = "30 observations"
    st.rerun()

fc = get_forecast_for_horizon(forecast_df, selected_horizon)

st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)

# ── Selected horizon KPI metrics ──────────────────────────────────────────────
if fc is not None:
    c1, c2, c3, c4, c5 = st.columns(5, gap="small")
    direction = fc["direction"]
    dcolor = direction_color(direction)
    arrow  = direction_arrow(direction)

    with c1:
        st.metric("Current BDI", fmt_number(fc["current_bdi"], 0))
    with c2:
        st.metric("Forecasted BDI", fmt_number(fc["forecasted_bdi"], 2))
    with c3:
        st.metric("Absolute Change", fmt_change(fc["change"], 2))
    with c4:
        st.metric("% Change", fmt_pct(fc["pct_change"], 2))
    with c5:
        st.markdown(
            f"""<div class='fiq-card' style='height:100px; padding:0.75rem 1rem;'>
                <div class='fiq-label'>Forecast Direction</div>
                <div style='font-size:1.4rem; font-weight:800; color:{dcolor}; line-height:1.2;'>{arrow}</div>
                <div style='font-size:0.75rem; color:{dcolor}; font-weight:700;'>{direction}</div>
            </div>""",
            unsafe_allow_html=True,
        )
else:
    st.warning(f"Forecast for horizon '{selected_horizon}' not found in data.")

st.markdown("<div style='margin-top:1.25rem;'></div>", unsafe_allow_html=True)

# ── Horizon chart ────────────────────────────────────────────────────────────
if cleaned_df is not None and fc is not None:
    fig = build_horizon_chart(cleaned_df, fc, selected_horizon)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True})

# ── Full comparison chart (expander) ──────────────────────────────────────────
with st.expander("Show All Horizons — Combined Historical & Forecast Chart", expanded=False):
    if cleaned_df is not None:
        fig2 = build_bdi_forecast_chart(
            cleaned_df, forecasts,
            title="BDI Historical Trend & All Forecast Horizons",
        )
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": True})

st.markdown("---")

# ── Forecast table ────────────────────────────────────────────────────────────
st.markdown("<div class='fiq-section-title'>Forecast Summary Table</div>", unsafe_allow_html=True)
render_forecast_table(forecasts)

st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
render_disclaimer()
render_footer()
