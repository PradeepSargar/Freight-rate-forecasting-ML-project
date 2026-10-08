"""
FreightIQ — Page 04: Model Performance & Validation
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
        page_title="Model Performance — FreightIQ",
        page_icon="🎯",
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

from utils.data_loader import load_feature_engineered
from utils.forecasting import HORIZON_METRICS, get_performance_table, get_feature_importance
from components.header import render_hero, render_section_header, render_disclaimer, render_footer
from components.charts import build_feature_importance_chart, build_performance_chart

# Load data for feature importance (from saved model or fallback)
feat_eng_df = load_feature_engineered()

render_hero(
    title="Model Performance & Validation",
    subtitle="XGBoost Regression validation results across time-based holdout and TimeSeriesSplit cross-validation.",
    badge_text="MODEL PERFORMANCE",
    meta_items=[
        ("Algorithm", "XGBoost Regression"),
        ("Validation", "Time-Based Holdout + TimeSeriesSplit"),
        ("Target", "Future BDI"),
        ("Horizons", "7 / 14 / 30 Observations"),
    ],
)

# ── Section 1: Holdout Performance ───────────────────────────────────────────
st.markdown(
    "<div class='fiq-section-title'>Holdout Performance</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='fiq-muted' style='margin-bottom:0.75rem;'>Evaluation on a reserved time-based holdout set "
    "not seen during training.</div>",
    unsafe_allow_html=True,
)

holdout_data = []
for horizon, metrics in HORIZON_METRICS.items():
    n = horizon.split()[0]
    m = metrics["holdout"]
    holdout_data.append({
        "Horizon": f"{n} Observations",
        "MAE": m["MAE"],
        "RMSE": m["RMSE"],
        "MAPE (%)": m["MAPE"],
    })

holdout_df = pd.DataFrame(holdout_data)
st.dataframe(
    holdout_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Horizon":   st.column_config.TextColumn("Horizon", width="medium"),
        "MAE":       st.column_config.NumberColumn("MAE", format="%.2f"),
        "RMSE":      st.column_config.NumberColumn("RMSE", format="%.2f"),
        "MAPE (%)":  st.column_config.NumberColumn("MAPE (%)", format="%.2f%%"),
    },
)

# Holdout metric cards
cols = st.columns(3, gap="small")
for col, row in zip(cols, holdout_data):
    with col:
        st.markdown(
            f"""
            <div class="fiq-card">
                <div class="fiq-label">{row['Horizon']}</div>
                <div style="margin-top:0.75rem; display:grid;
                            grid-template-columns:1fr 1fr 1fr; gap:0.5rem;">
                    <div>
                        <div style="font-size:0.62rem; color:#64748B; text-transform:uppercase;
                                    letter-spacing:0.08em;">MAE</div>
                        <div style="font-size:1.1rem; font-weight:700; color:#38BDF8;">
                            {row['MAE']:,.2f}
                        </div>
                    </div>
                    <div>
                        <div style="font-size:0.62rem; color:#64748B; text-transform:uppercase;
                                    letter-spacing:0.08em;">RMSE</div>
                        <div style="font-size:1.1rem; font-weight:700; color:#F59E0B;">
                            {row['RMSE']:,.2f}
                        </div>
                    </div>
                    <div>
                        <div style="font-size:0.62rem; color:#64748B; text-transform:uppercase;
                                    letter-spacing:0.08em;">MAPE</div>
                        <div style="font-size:1.1rem; font-weight:700; color:#22C55E;">
                            {row['MAPE (%)']:.2f}%
                        </div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")

# ── Section 2: TimeSeriesSplit Performance ────────────────────────────────────
st.markdown(
    "<div class='fiq-section-title'>TimeSeriesSplit Cross-Validation Performance</div>",
    unsafe_allow_html=True,
)
st.markdown(
    "<div class='fiq-muted' style='margin-bottom:0.75rem;'>Walk-forward cross-validation "
    "preserving temporal ordering.</div>",
    unsafe_allow_html=True,
)

tss_data = []
for horizon, metrics in HORIZON_METRICS.items():
    n = horizon.split()[0]
    m = metrics["tss"]
    tss_data.append({
        "Horizon": f"{n} Observations",
        "MAE": m["MAE"],
        "RMSE": m["RMSE"],
        "MAPE (%)": m["MAPE"],
    })

tss_df = pd.DataFrame(tss_data)
st.dataframe(
    tss_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Horizon":   st.column_config.TextColumn("Horizon", width="medium"),
        "MAE":       st.column_config.NumberColumn("MAE", format="%.2f"),
        "RMSE":      st.column_config.NumberColumn("RMSE", format="%.2f"),
        "MAPE (%)":  st.column_config.NumberColumn("MAPE (%)", format="%.2f%%"),
    },
)

# Combined chart
perf_rows = get_performance_table()
fig_perf = build_performance_chart(perf_rows)
if fig_perf:
    st.plotly_chart(fig_perf, use_container_width=True, config={"displayModeBar": False})

st.markdown("---")

# ── Section 3: Model Architecture ────────────────────────────────────────────
st.markdown(
    "<div class='fiq-section-title'>Model Architecture</div>",
    unsafe_allow_html=True,
)

arch_col1, arch_col2 = st.columns([1, 2], gap="large")

with arch_col1:
    st.markdown(
        """
        <div class="fiq-card">
            <div class="fiq-label">Architecture Details</div>
            <div style="margin-top:1rem; display:flex; flex-direction:column; gap:0.75rem;">
                <div>
                    <div style="font-size:0.62rem; color:#64748B; text-transform:uppercase; letter-spacing:0.08em;">Algorithm</div>
                    <div style="font-size:0.9rem; font-weight:600; color:#F8FAFC; margin-top:2px;">XGBoost Regression</div>
                </div>
                <div>
                    <div style="font-size:0.62rem; color:#64748B; text-transform:uppercase; letter-spacing:0.08em;">Target Variable</div>
                    <div style="font-size:0.9rem; font-weight:600; color:#F8FAFC; margin-top:2px;">Future BDI</div>
                </div>
                <div>
                    <div style="font-size:0.62rem; color:#64748B; text-transform:uppercase; letter-spacing:0.08em;">Forecast Horizons</div>
                    <div style="font-size:0.9rem; font-weight:600; color:#F8FAFC; margin-top:2px;">7 / 14 / 30 Observations</div>
                </div>
                <div>
                    <div style="font-size:0.62rem; color:#64748B; text-transform:uppercase; letter-spacing:0.08em;">Training Data</div>
                    <div style="font-size:0.9rem; font-weight:600; color:#F8FAFC; margin-top:2px;">3,204 samples</div>
                </div>
                <div>
                    <div style="font-size:0.62rem; color:#64748B; text-transform:uppercase; letter-spacing:0.08em;">Features</div>
                    <div style="font-size:0.9rem; font-weight:600; color:#F8FAFC; margin-top:2px;">33 engineered features</div>
                </div>
                <div>
                    <div style="font-size:0.62rem; color:#64748B; text-transform:uppercase; letter-spacing:0.08em;">Validation Strategy</div>
                    <div style="font-size:0.9rem; font-weight:600; color:#F8FAFC; margin-top:2px;">Time-Based Split + TimeSeriesSplit</div>
                </div>
                <div>
                    <div style="font-size:0.62rem; color:#64748B; text-transform:uppercase; letter-spacing:0.08em;">Metrics</div>
                    <div style="font-size:0.9rem; font-weight:600; color:#F8FAFC; margin-top:2px;">MAE · RMSE · MAPE</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with arch_col2:
    # Input features info
    st.markdown(
        """
        <div class="fiq-card">
            <div class="fiq-label">Feature Categories</div>
            <div style="margin-top:1rem; display:grid; grid-template-columns:1fr 1fr; gap:1rem;">
                <div>
                    <div style="font-size:0.72rem; color:#38BDF8; font-weight:700;
                                margin-bottom:0.4rem;">Freight Indices</div>
                    <div style="font-size:0.78rem; color:#94A3B8; line-height:1.8;">
                        BDI · BCI · BPI · BSI<br>
                        Lag features (1, 7 obs)<br>
                        Rolling means (7, 14, 30)
                    </div>
                </div>
                <div>
                    <div style="font-size:0.72rem; color:#22C55E; font-weight:700;
                                margin-bottom:0.4rem;">Commodity Prices</div>
                    <div style="font-size:0.78rem; color:#94A3B8; line-height:1.8;">
                        Brent Crude<br>
                        Coal<br>
                        Iron Ore<br>
                        Lag features (1, 7 obs)
                    </div>
                </div>
                <div>
                    <div style="font-size:0.72rem; color:#F59E0B; font-weight:700;
                                margin-bottom:0.4rem;">Economic Indicators</div>
                    <div style="font-size:0.78rem; color:#94A3B8; line-height:1.8;">
                        USD/INR Exchange Rate<br>
                        Lag features (1, 7 obs)
                    </div>
                </div>
                <div>
                    <div style="font-size:0.72rem; color:#A78BFA; font-weight:700;
                                margin-bottom:0.4rem;">Date Features</div>
                    <div style="font-size:0.78rem; color:#94A3B8; line-height:1.8;">
                        Year · Month · Quarter<br>
                        Day of Week
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ── Section 4: Feature Importance ────────────────────────────────────────────
st.markdown(
    "<div class='fiq-section-title'>Top Freight Forecasting Features</div>",
    unsafe_allow_html=True,
)

selected_horizon = st.session_state.get("forecast_horizon", 7)
selected_h = f"{selected_horizon} observations"
fi = get_feature_importance(selected_h)

if fi is not None and fi:
    fig_fi = build_feature_importance_chart(fi, top_n=15)
    if fig_fi:
        st.plotly_chart(fig_fi, use_container_width=True, config={"displayModeBar": False})
else:
    # Fallback: show feature list from feature-engineered dataset
    if feat_eng_df is not None:
        exclude = {"Date", "BDI", "BCI", "BPI", "BSI", "Brent", "USD_INR",
                   "Coal", "Iron_Ore", "BDI_Target"}
        feature_cols = [c for c in feat_eng_df.columns if c not in exclude]
        st.markdown(
            f"""
            <div class="fiq-insight-box">
                <strong>Feature Importance Note:</strong> No pre-trained XGBoost model artifact
                found in <code>models/forecasting/</code>. Feature importance cannot be extracted
                without the saved model. The dataset contains <strong>{len(feature_cols)}</strong>
                engineered features listed below.
            </div>
            """,
            unsafe_allow_html=True,
        )
        feat_df = pd.DataFrame({"Feature Name": feature_cols})
        st.dataframe(feat_df, use_container_width=True, hide_index=True, height=350)
    else:
        st.info(
            "Feature importance is not available. "
            "Save the trained XGBoost model to `models/forecasting/xgb_7obs.json` "
            "(and similarly for 14/30) to enable this section."
        )

st.markdown("<div style='margin-top:1rem;'></div>", unsafe_allow_html=True)
render_disclaimer()
render_footer()
