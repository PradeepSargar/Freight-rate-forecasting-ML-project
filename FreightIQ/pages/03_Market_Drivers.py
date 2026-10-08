"""
FreightIQ — Page 03: Market Drivers
"""
import sys, os
from pathlib import Path
_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

import streamlit as st
import pandas as pd

try:
    st.set_page_config(
        page_title="Market Drivers — FreightIQ",
        page_icon="📉",
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

from utils.data_loader import load_cleaned_dataset, get_correlation_matrix
from components.header import render_hero, render_section_header, render_disclaimer, render_footer
from components.charts import (
    build_indicator_chart,
    build_multi_indicator_chart,
    build_correlation_heatmap,
)

cleaned_df = load_cleaned_dataset()
corr_df    = get_correlation_matrix(cleaned_df)

render_hero(
    title="Market Drivers",
    subtitle="Historical trends in freight indices, commodity prices, and macroeconomic indicators that influence BDI.",
    badge_text="MARKET DRIVERS",
)

if cleaned_df is None:
    st.error("Dataset not found. Expected: data/processed/model1_cleaned_dataset.csv")
    st.stop()

COLOR_MAP = {
    "BDI": "#38BDF8",
    "BCI": "#22C55E",
    "BPI": "#F59E0B",
    "BSI": "#A78BFA",
    "Brent": "#EF4444",
    "USD_INR": "#FB923C",
    "Coal": "#94A3B8",
    "Iron_Ore": "#34D399",
}

LABEL_MAP = {
    "BDI": "Baltic Dry Index",
    "BCI": "Baltic Capesize Index",
    "BPI": "Baltic Panamax Index",
    "BSI": "Baltic Supramax Index",
    "Brent": "Brent Crude (USD/bbl)",
    "USD_INR": "USD/INR Exchange Rate",
    "Coal": "Coal Price (USD/t)",
    "Iron_Ore": "Iron Ore Price (USD/t)",
}

# Dry Bulk Indices
st.markdown("<div class='fiq-section-title'>Dry Bulk Freight Indices</div>", unsafe_allow_html=True)
st.markdown("<div class='fiq-muted'>BDI, BCI, BPI, and BSI — Baltic Exchange indices tracking global dry-bulk shipping demand.</div>", unsafe_allow_html=True)
st.markdown("<div style='margin-bottom:0.75rem;'></div>", unsafe_allow_html=True)

fig_indices = build_multi_indicator_chart(
    cleaned_df,
    ["BDI", "BCI", "BPI", "BSI"],
    "Dry Bulk Indices — Historical Comparison",
    height=350,
)
if fig_indices:
    st.plotly_chart(fig_indices, use_container_width=True, config={"displayModeBar": True})

cols = st.columns(2)
for i, col_key in enumerate(["BDI", "BCI", "BPI", "BSI"]):
    with cols[i % 2]:
        fig = build_indicator_chart(
            cleaned_df, col_key, LABEL_MAP[col_key],
            color=COLOR_MAP[col_key], height=240,
        )
        if fig:
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

st.markdown("---")

# Commodity Drivers
st.markdown("<div class='fiq-section-title'>Commodity Drivers</div>", unsafe_allow_html=True)
st.markdown("<div class='fiq-muted'>Iron Ore and Coal — primary dry-bulk cargo commodities driving freight demand.</div>", unsafe_allow_html=True)
st.markdown("<div style='margin-bottom:0.75rem;'></div>", unsafe_allow_html=True)

cols2 = st.columns(2)
for i, col_key in enumerate(["Iron_Ore", "Coal"]):
    with cols2[i]:
        fig = build_indicator_chart(
            cleaned_df, col_key, LABEL_MAP[col_key],
            color=COLOR_MAP[col_key], height=280,
        )
        if fig:
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True})

st.markdown("---")

# Macro / Energy
st.markdown("<div class='fiq-section-title'>Macro & Energy Drivers</div>", unsafe_allow_html=True)
st.markdown("<div class='fiq-muted'>Brent Crude and USD/INR — energy costs and currency dynamics influencing global freight economics.</div>", unsafe_allow_html=True)
st.markdown("<div style='margin-bottom:0.75rem;'></div>", unsafe_allow_html=True)

cols3 = st.columns(2)
for i, col_key in enumerate(["Brent", "USD_INR"]):
    with cols3[i]:
        fig = build_indicator_chart(
            cleaned_df, col_key, LABEL_MAP[col_key],
            color=COLOR_MAP[col_key], height=280,
        )
        if fig:
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": True})

st.markdown("---")

# Correlation Matrix
st.markdown("<div class='fiq-section-title'>Correlation Matrix</div>", unsafe_allow_html=True)
st.markdown("<div class='fiq-muted'>Pearson correlations among freight indices, commodity prices, and macroeconomic indicators (computed from historical data).</div>", unsafe_allow_html=True)
st.markdown("<div style='margin-bottom:0.75rem;'></div>", unsafe_allow_html=True)

if corr_df is not None:
    fig_corr = build_correlation_heatmap(corr_df)
    if fig_corr:
        st.plotly_chart(fig_corr, use_container_width=True, config={"displayModeBar": False})

    st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
    st.markdown("<div class='fiq-section-title'>Key BDI Correlations</div>", unsafe_allow_html=True)
    if "BDI" in corr_df.columns:
        bdi_corr = (
            corr_df["BDI"]
            .drop("BDI", errors="ignore")
            .abs()
            .sort_values(ascending=False)
        )
        corr_display = pd.DataFrame({
            "Indicator": [LABEL_MAP.get(k, k) for k in bdi_corr.index],
            "Correlation with BDI": [f"{corr_df['BDI'][k]:.3f}" for k in bdi_corr.index],
            "Absolute Strength": [f"{v:.3f}" for v in bdi_corr.values],
        })
        st.dataframe(corr_display, use_container_width=True, hide_index=True)
else:
    st.info("Correlation data unavailable.")

render_disclaimer()
render_footer()
