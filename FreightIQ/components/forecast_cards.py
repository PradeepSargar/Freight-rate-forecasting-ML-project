"""
FreightIQ — Forecast Cards Component
Renders Short/Medium/Longer-Term forecast cards with dynamic values.
"""

from __future__ import annotations

import streamlit as st
from utils.formatting import fmt_number, fmt_pct, fmt_change, direction_arrow, direction_color


HORIZON_META = [
    ("7 observations",  "SHORT TERM",   "7 Observations"),
    ("14 observations", "MEDIUM TERM",  "14 Observations"),
    ("30 observations", "LONGER TERM",  "30 Observations"),
]


def render_forecast_cards(forecasts: list[dict | None]) -> None:
    """Render 3-column forecast summary cards."""
    cols = st.columns(3, gap="medium")

    for col, (h_key, term_label, obs_label), fc in zip(cols, HORIZON_META, forecasts):
        with col:
            if fc is None:
                st.markdown(
                    f"""
                    <div class="fiq-card">
                        <div class="fiq-label">{term_label}</div>
                        <div style="font-size:0.8rem; color:#64748B; margin-top:0.3rem;">{obs_label}</div>
                        <div style="margin-top:1rem; color:#64748B;">Data unavailable</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                continue

            direction = fc["direction"]
            color = direction_color(direction)
            arrow = direction_arrow(direction)
            bdi_val = fmt_number(fc["forecasted_bdi"], 2)
            change_str = fmt_change(fc["change"], 2)
            pct_str = fmt_pct(fc["pct_change"], 2)

            badge_color = (
                "#22C55E" if direction == "Increasing"
                else "#EF4444" if direction == "Decreasing"
                else "#F59E0B"
            )
            badge_bg = (
                "#052E16" if direction == "Increasing"
                else "#2D0707" if direction == "Decreasing"
                else "#2D1D00"
            )

            st.markdown(
                f"""
                <div class="fiq-card">
                    <div class="fiq-label">{term_label}</div>
                    <div style="font-size:0.78rem; color:#64748B; margin-top:0.1rem;">{obs_label}</div>
                    <div style="margin-top:1rem;">
                        <div style="font-size:0.65rem; color:#64748B; text-transform:uppercase;
                                    letter-spacing:0.08em;">Forecast</div>
                        <div style="font-size:1.75rem; font-weight:800; color:#F8FAFC;
                                    line-height:1.1; margin-top:0.2rem;">{bdi_val}</div>
                    </div>
                    <div style="margin-top:0.75rem; display:flex; gap:1rem;">
                        <div>
                            <div style="font-size:0.65rem; color:#64748B; text-transform:uppercase;
                                        letter-spacing:0.08em;">Change</div>
                            <div style="font-size:0.9rem; font-weight:600; color:{color};
                                        margin-top:0.1rem;">{change_str}</div>
                        </div>
                        <div>
                            <div style="font-size:0.65rem; color:#64748B; text-transform:uppercase;
                                        letter-spacing:0.08em;">% Change</div>
                            <div style="font-size:0.9rem; font-weight:600; color:{color};
                                        margin-top:0.1rem;">{pct_str}</div>
                        </div>
                    </div>
                    <div style="margin-top:0.75rem;">
                        <span style="background:{badge_bg}; color:{badge_color};
                                     border:1px solid {badge_color}; border-radius:4px;
                                     padding:2px 8px; font-size:0.68rem; font-weight:700;
                                     letter-spacing:0.08em; text-transform:uppercase;">
                            {arrow} {direction}
                        </span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_forecast_table(forecasts: list[dict | None]) -> None:
    """Render a clean professional forecast comparison table."""
    import pandas as pd

    rows = []
    for fc in forecasts:
        if fc is None:
            continue
        n = fc["horizon"].split()[0]
        rows.append({
            "Horizon": f"{n} Observations",
            "Current BDI": fmt_number(fc["current_bdi"], 0),
            "Forecasted BDI": fmt_number(fc["forecasted_bdi"], 2),
            "Change": fmt_change(fc["change"], 2),
            "% Change": fmt_pct(fc["pct_change"], 2),
            "Direction": f"{direction_arrow(fc['direction'])} {fc['direction']}",
        })

    if not rows:
        st.info("Forecast data unavailable.")
        return

    df = pd.DataFrame(rows)
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Horizon":        st.column_config.TextColumn("Horizon", width="medium"),
            "Current BDI":    st.column_config.TextColumn("Current BDI"),
            "Forecasted BDI": st.column_config.TextColumn("Forecasted BDI"),
            "Change":         st.column_config.TextColumn("Change"),
            "% Change":       st.column_config.TextColumn("% Change"),
            "Direction":      st.column_config.TextColumn("Direction"),
        },
    )
