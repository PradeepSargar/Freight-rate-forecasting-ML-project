"""
FreightIQ — Page 05: Methodology
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
        page_title="Methodology — FreightIQ",
        page_icon="📋",
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

from components.header import render_hero, render_disclaimer, render_footer


render_hero(
    title="Methodology",
    subtitle="Model development pipeline, data sources, feature engineering, and validation strategy.",
    badge_text="METHODOLOGY",
)

# ── Pipeline Visual ───────────────────────────────────────────────────────────
st.markdown(
    "<div class='fiq-section-title'>Modeling Pipeline</div>",
    unsafe_allow_html=True,
)

PIPELINE_STEPS = [
    ("Raw Data",              "#38BDF8", "Historical Baltic Exchange indices, commodity prices, and economic indicators (2012–2025)."),
    ("Data Cleaning",         "#38BDF8", "Handling missing values, outlier identification, and date alignment across multiple sources."),
    ("Data Integration",      "#38BDF8", "Merging all indicator series into a unified daily panel dataset."),
    ("Feature Engineering",   "#22C55E", "Lag features (1, 7 obs), rolling means (7, 14, 30 obs), date features, and cross-indicator lags."),
    ("Leakage Prevention",    "#22C55E", "Target shift validation to ensure no future BDI information leaked into input features."),
    ("Time-Based Validation", "#F59E0B", "Strict temporal train/holdout split + TimeSeriesSplit cross-validation preserving chronological order."),
    ("XGBoost Training",      "#A78BFA", "Three separate XGBoost Regressor models trained per forecast horizon (7 / 14 / 30 observations)."),
    ("7 / 14 / 30 Forecasts", "#EF4444", "Final BDI forecasts generated from the latest available market data."),
]

pipeline_html = '<div style="display:flex; flex-direction:column; gap:0; max-width:680px;">'
for i, (step, color, desc) in enumerate(PIPELINE_STEPS):
    connector = (
        f'<div style="width:2px; height:16px; background:{color}; margin-left:19px; opacity:0.5;"></div>'
        if i < len(PIPELINE_STEPS) - 1
        else ""
    )
    pipeline_html += f"""
    <div style="display:flex; align-items:flex-start; gap:12px;">
        <div style="flex-shrink:0; width:38px; height:38px; border-radius:50%;
                    background:#151E2E; border:2px solid {color};
                    display:flex; align-items:center; justify-content:center;
                    font-size:0.75rem; font-weight:700; color:{color};">{i+1}</div>
        <div style="flex:1; padding-bottom:4px;">
            <div style="font-size:0.85rem; font-weight:700; color:#F8FAFC;">{step}</div>
            <div style="font-size:0.75rem; color:#94A3B8; margin-top:2px; line-height:1.5;">{desc}</div>
        </div>
    </div>
    {connector}
    """
pipeline_html += "</div>"
st.markdown(pipeline_html, unsafe_allow_html=True)

st.markdown("---")

# ── Problem Statement ─────────────────────────────────────────────────────────
st.markdown("<div class='fiq-section-title'>Problem Statement</div>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="fiq-card">
    <p style="color:#94A3B8; font-size:0.9rem; line-height:1.8; margin:0;">
    The Baltic Dry Index (BDI) is a composite measure of global dry-bulk shipping costs across
    major routes and vessel categories (Capesize, Panamax, Supramax). It serves as a leading
    economic indicator and is closely watched by commodity traders, shipping companies, and
    macroeconomic analysts.<br><br>
    FreightIQ addresses the problem of forecasting the BDI across three distinct time horizons
    (7, 14, and 30 observations) using a machine learning approach grounded in historical
    freight-market data and associated economic indicators.
    The fundamental challenge is the high volatility, regime shifts, and non-linear dynamics
    of freight markets — conditions that make simple extrapolation inadequate and motivate a
    feature-rich, tree-based regression approach.
    </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# ── Data Sources ──────────────────────────────────────────────────────────────
st.markdown("<div class='fiq-section-title'>Data Sources</div>", unsafe_allow_html=True)

src_cols = st.columns(2, gap="medium")

with src_cols[0]:
    st.markdown(
        """
        <div class="fiq-card">
            <div class="fiq-label" style="color:#38BDF8; border-bottom:1px solid #1E2940;
                                          padding-bottom:0.5rem; margin-bottom:0.75rem;">
                Freight Indices (Baltic Exchange)
            </div>
            <div style="font-size:0.78rem; color:#94A3B8; line-height:2;">
                <div>
                    <span style="color:#38BDF8; font-weight:600;">BDI</span>
                    &nbsp;—&nbsp; Baltic Dry Index
                    <span class="fiq-badge" style="margin-left:4px; font-size:0.58rem;">PRIMARY TARGET</span>
                </div>
                <div>
                    <span style="color:#22C55E; font-weight:600;">BCI</span>
                    &nbsp;—&nbsp; Baltic Capesize Index
                </div>
                <div>
                    <span style="color:#F59E0B; font-weight:600;">BPI</span>
                    &nbsp;—&nbsp; Baltic Panamax Index
                </div>
                <div>
                    <span style="color:#A78BFA; font-weight:600;">BSI</span>
                    &nbsp;—&nbsp; Baltic Supramax Index
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with src_cols[1]:
    st.markdown(
        """
        <div class="fiq-card">
            <div class="fiq-label" style="color:#22C55E; border-bottom:1px solid #1E2940;
                                          padding-bottom:0.5rem; margin-bottom:0.75rem;">
                Supporting Indicators
            </div>
            <div style="font-size:0.78rem; color:#94A3B8; line-height:2;">
                <div>
                    <span style="color:#EF4444; font-weight:600;">Brent Crude</span>
                    &nbsp;—&nbsp; Energy / bunker fuel proxy
                </div>
                <div>
                    <span style="color:#FB923C; font-weight:600;">USD/INR</span>
                    &nbsp;—&nbsp; Currency dynamics
                </div>
                <div>
                    <span style="color:#94A3B8; font-weight:600;">Coal</span>
                    &nbsp;—&nbsp; Dry-bulk cargo demand
                </div>
                <div>
                    <span style="color:#34D399; font-weight:600;">Iron Ore</span>
                    &nbsp;—&nbsp; Dry-bulk cargo demand
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ── Feature Engineering ───────────────────────────────────────────────────────
st.markdown("<div class='fiq-section-title'>Feature Engineering</div>", unsafe_allow_html=True)
fe_cols = st.columns(3, gap="medium")

fe_items = [
    ("Lag Features", "#38BDF8", [
        "BDI_Lag_1, BDI_Lag_7, BDI_Lag_14, BDI_Lag_30",
        "BCI_Lag_1, BCI_Lag_7",
        "BPI_Lag_1, BPI_Lag_7",
        "BSI_Lag_1, BSI_Lag_7",
        "Brent_Lag_1, Brent_Lag_7",
        "USD_INR_Lag_1, USD_INR_Lag_7",
        "Coal_Lag_1, Coal_Lag_7",
        "Iron_Ore_Lag_1, Iron_Ore_Lag_7",
    ]),
    ("Rolling Averages", "#22C55E", [
        "BDI_Rolling_Mean_7",
        "BDI_Rolling_Mean_14",
        "BDI_Rolling_Mean_30",
    ]),
    ("Date Features", "#F59E0B", [
        "Year",
        "Month",
        "Quarter",
        "Day_of_Week",
    ]),
]

for col, (title, color, items) in zip(fe_cols, fe_items):
    with col:
        items_html = "".join(
            f'<div style="font-size:0.75rem; color:#94A3B8; padding:3px 0; '
            f'border-bottom:1px solid #1A2235;">{item}</div>'
            for item in items
        )
        st.markdown(
            f"""
            <div class="fiq-card">
                <div style="font-size:0.72rem; color:{color}; font-weight:700;
                            text-transform:uppercase; letter-spacing:0.08em;
                            margin-bottom:0.6rem;">{title}</div>
                {items_html}
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")

# ── Leakage Prevention ────────────────────────────────────────────────────────
st.markdown("<div class='fiq-section-title'>Leakage Prevention</div>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="fiq-card">
    <p style="color:#94A3B8; font-size:0.88rem; line-height:1.9; margin:0;">
    A critical concern in time-series forecasting is data leakage — when information from
    the future inadvertently enters the training feature set. FreightIQ addresses this through:
    </p>
    <ul style="color:#94A3B8; font-size:0.85rem; line-height:2; margin-top:0.5rem;">
        <li><strong style="color:#F8FAFC;">Strict lag construction:</strong>
            All lag features reference only past observations relative to the
            current data point.</li>
        <li><strong style="color:#F8FAFC;">Target shift validation:</strong>
            The BDI_Target column is created by forward-shifting the BDI series
            by the forecast horizon (7, 14, or 30 steps), ensuring the target
            represents a genuinely future value.</li>
        <li><strong style="color:#F8FAFC;">Rolling features:</strong>
            Rolling means use only past data (not centered, not future-inclusive).</li>
        <li><strong style="color:#F8FAFC;">Leakage check status:</strong>
            <span class="fiq-badge fiq-badge-green">PASSED</span></li>
    </ul>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("---")

# ── Validation Strategy ───────────────────────────────────────────────────────
st.markdown("<div class='fiq-section-title'>Time-Based Validation Strategy</div>", unsafe_allow_html=True)

val_col1, val_col2 = st.columns(2, gap="medium")

with val_col1:
    st.markdown(
        """
        <div class="fiq-card">
            <div style="font-size:0.72rem; color:#38BDF8; font-weight:700;
                        text-transform:uppercase; letter-spacing:0.08em;
                        margin-bottom:0.6rem;">Time-Based Holdout</div>
            <p style="color:#94A3B8; font-size:0.82rem; line-height:1.8; margin:0;">
                A fixed proportion of the most recent data is withheld entirely
                from training and used only for final evaluation. This simulates
                real-world deployment where the model has never seen the most
                recent market conditions.
            </p>
            <div style="margin-top:0.75rem;">
                <span class="fiq-badge">Temporal Integrity: MAINTAINED</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with val_col2:
    st.markdown(
        """
        <div class="fiq-card">
            <div style="font-size:0.72rem; color:#22C55E; font-weight:700;
                        text-transform:uppercase; letter-spacing:0.08em;
                        margin-bottom:0.6rem;">TimeSeriesSplit Cross-Validation</div>
            <p style="color:#94A3B8; font-size:0.82rem; line-height:1.8; margin:0;">
                Walk-forward cross-validation using <code>sklearn.TimeSeriesSplit</code>.
                Each fold expands the training window chronologically, preventing any
                future data from entering the training set. This provides a robust
                estimate of out-of-sample performance across multiple market regimes.
            </p>
            <div style="margin-top:0.75rem;">
                <span class="fiq-badge fiq-badge-green">Regime Coverage: MULTI-FOLD</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ── Data Quality Status ───────────────────────────────────────────────────────
st.markdown("<div class='fiq-section-title'>Data Quality Status</div>", unsafe_allow_html=True)

quality_items = [
    ("Missing Values", "0", "#22C55E", "fiq-badge-green"),
    ("Leakage Check", "PASSED", "#22C55E", "fiq-badge-green"),
    ("Temporal Ordering", "MAINTAINED", "#22C55E", "fiq-badge-green"),
    ("Feature Engineering", "COMPLETED", "#22C55E", "fiq-badge-green"),
    ("Forecast Horizons", "3", "#38BDF8", "fiq-badge"),
]
q_cols = st.columns(5, gap="small")
for col, (label, value, color, badge_cls) in zip(q_cols, quality_items):
    with col:
        st.markdown(
            f"""
            <div class="fiq-card" style="height:100px; text-align:center; padding:1rem;">
                <div class="fiq-label" style="margin-bottom:0.4rem;">{label}</div>
                <span class="{badge_cls}">{value}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")

# ── Forecast Generation ───────────────────────────────────────────────────────
st.markdown("<div class='fiq-section-title'>Forecast Generation</div>", unsafe_allow_html=True)
st.markdown(
    """
    <div class="fiq-card">
    <p style="color:#94A3B8; font-size:0.88rem; line-height:1.9; margin:0;">
    Three independent XGBoost Regressor models are trained — one per forecast horizon.
    Each model learns to predict a shifted version of the BDI (the BDI n steps ahead)
    using the full engineered feature set.<br><br>
    Final forecasts are generated by feeding the most recent observation's feature vector
    into each trained model. The output is a point estimate for the expected BDI level
    at each horizon.
    </p>
    <div style="margin-top:1rem; display:flex; gap:0.75rem; flex-wrap:wrap;">
        <span class="fiq-badge">7-Observation Model</span>
        <span class="fiq-badge">14-Observation Model</span>
        <span class="fiq-badge">30-Observation Model</span>
    </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
render_disclaimer()
render_footer()
