"""
FreightIQ — Sidebar Component
Renders a premium sidebar with branding, nav, model status, and horizon selector.
"""

import streamlit as st


HORIZONS = ["7 observations", "14 observations", "30 observations"]


def render_sidebar_top() -> None:
    """Render the top brand block in the sidebar."""
    with st.sidebar:
        st.markdown(
            """
            <div style="padding: 0.5rem 0 1rem 0;">
                <div style="font-size:1.3rem; font-weight:800; color:#F8FAFC;
                            letter-spacing:0.06em; line-height:1.2;">
                    FREIGHTIQ
                </div>
                <div style="font-size:0.72rem; color:#64748B; margin-top:3px;
                            letter-spacing:0.04em;">
                    Intelligent Freight Forecasting
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_sidebar_bottom() -> None:
    """Render the model status, horizon selector, and info block below navigation."""
    with st.sidebar:
        st.markdown(
            """
            <div style="margin-top:0.5rem; margin-bottom:0.75rem; padding-top:0.75rem;
                        border-top:1px solid #1E2940;">
                <div style="display:flex; align-items:center; gap:6px;">
                    <span style="color:#22C55E; font-size:0.75rem;">●</span>
                    <span style="font-size:0.7rem; font-weight:700; color:#94A3B8;
                                 letter-spacing:0.1em; text-transform:uppercase;">
                        Model Active
                    </span>
                    <span style="font-size:0.65rem; color:#64748B; margin-left:auto;">
                        XGBoost
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Horizon selector ────────────────────────────────────────────────
        st.markdown(
            "<div style='font-size:0.68rem; color:#64748B; text-transform:uppercase; "
            "letter-spacing:0.08em; margin-bottom:0.4rem;'>Forecast Horizon</div>",
            unsafe_allow_html=True,
        )

        current_horizon = st.session_state.get("selected_horizon", "7 observations")
        default_idx = HORIZONS.index(current_horizon) if current_horizon in HORIZONS else 0

        selected_horizon = st.radio(
            label="forecast_horizon_sidebar",
            options=HORIZONS,
            format_func=lambda x: x.replace("observations", "Obs"),
            index=default_idx,
            label_visibility="collapsed",
            key="sidebar_horizon_radio",
        )
        st.session_state["selected_horizon"] = selected_horizon

        # ── Model info block ────────────────────────────────────────────────
        st.markdown(
            """
            <div style="margin-top:1.25rem; padding-top:0.75rem; border-top:1px solid #1E2940;">
                <div style="font-size:0.68rem; color:#64748B; text-transform:uppercase;
                            letter-spacing:0.08em; margin-bottom:0.5rem;">Model Info</div>
                <div style="font-size:0.76rem; color:#94A3B8; line-height:1.8;">
                    <div><span style="color:#64748B;">Algorithm:</span> XGBoost</div>
                    <div><span style="color:#64748B;">Target:</span> BDI</div>
                    <div><span style="color:#64748B;">Date:</span> 06 Feb 2025</div>
                    <div><span style="color:#64748B;">Features:</span> 33</div>
                    <div><span style="color:#64748B;">Samples:</span> 3,204</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Footer ──────────────────────────────────────────────────────────
        st.markdown(
            """
            <div style="margin-top:1.5rem; padding-top:0.75rem; border-top:1px solid #1E2940;
                        font-size:0.65rem; color:#475569; text-align:left;">
                &copy; 2026 FreightIQ
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_sidebar() -> None:
    """Render the full sidebar (used when running pages standalone)."""
    render_sidebar_top()
    with st.sidebar:
        st.markdown(
            "<div style='font-size:0.68rem; color:#64748B; text-transform:uppercase; "
            "letter-spacing:0.08em; margin-bottom:0.5rem;'>Navigation</div>",
            unsafe_allow_html=True,
        )
    render_sidebar_bottom()
