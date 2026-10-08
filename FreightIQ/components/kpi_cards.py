"""
FreightIQ — KPI Cards Component
Renders professional metric cards for BDI, forecasts, and direction.
"""

from __future__ import annotations

import streamlit as st
from utils.formatting import fmt_number, fmt_pct, fmt_change, direction_arrow


def _delta_html(change: float, pct: float, direction: str) -> str:
    """Build colored delta string for st.metric delta_color workaround."""
    arrow = direction_arrow(direction)
    if direction == "Increasing":
        color = "#22C55E"
    elif direction == "Decreasing":
        color = "#EF4444"
    else:
        color = "#F59E0B"
    return f"<span style='color:{color};font-weight:600;'>{arrow} {fmt_change(change)} ({fmt_pct(pct)})</span>"


def render_kpi_cards(
    current_bdi: float | None,
    forecasts: list[dict | None],
    forecast_date: str | None,
) -> None:
    """
    Render the 5 KPI cards:
      Current BDI | 7-Obs Forecast | 14-Obs Forecast | 30-Obs Forecast | Direction
    """
    h7, h14, h30 = (forecasts + [None, None, None])[:3]

    cols = st.columns(5, gap="small")

    # ── Card 0: Current BDI ─────────────────────────────────────────────────
    with cols[0]:
        bdi_val = fmt_number(current_bdi, 0) if current_bdi is not None else "—"
        date_sub = forecast_date or "—"
        st.markdown(
            f"""
            <div class="fiq-card" style="height:130px;">
                <div class="fiq-label">Current BDI</div>
                <div class="fiq-value">{bdi_val}</div>
                <div class="fiq-muted" style="margin-top:0.4rem;">As of {date_sub}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # ── Cards 1–3: Horizon forecasts ─────────────────────────────────────────
    for i, (col, fc, label) in enumerate(
        zip(cols[1:4], [h7, h14, h30], ["7-Obs Forecast", "14-Obs Forecast", "30-Obs Forecast"])
    ):
        with col:
            if fc is None:
                st.markdown(
                    f"""<div class="fiq-card" style="height:130px;">
                        <div class="fiq-label">{label}</div>
                        <div class="fiq-value">—</div>
                        <div class="fiq-muted">Data unavailable</div>
                    </div>""",
                    unsafe_allow_html=True,
                )
            else:
                forecast_val = fmt_number(fc["forecasted_bdi"], 2)
                delta_html = _delta_html(fc["change"], fc["pct_change"], fc["direction"])
                st.markdown(
                    f"""
                    <div class="fiq-card" style="height:130px;">
                        <div class="fiq-label">{label}</div>
                        <div class="fiq-value">{forecast_val}</div>
                        <div style="margin-top:0.4rem;">{delta_html}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # ── Card 4: Direction ────────────────────────────────────────────────────
    with cols[4]:
        if h7 is not None:
            direction = h7["direction"]
            arrow = direction_arrow(direction)
            if direction == "Increasing":
                color = "#22C55E"
                badge_cls = "fiq-badge-green"
            elif direction == "Decreasing":
                color = "#EF4444"
                badge_cls = ""
            else:
                color = "#F59E0B"
                badge_cls = "fiq-badge-yellow"
        else:
            direction, arrow, color, badge_cls = "—", "—", "#94A3B8", ""

        st.markdown(
            f"""
            <div class="fiq-card" style="height:130px;">
                <div class="fiq-label">Forecast Direction</div>
                <div style="font-size:1.9rem; font-weight:800; color:{color};
                            line-height:1.2; margin-top:0.2rem;">{arrow}</div>
                <div style="margin-top:0.4rem;">
                    <span class="fiq-badge {badge_cls}">{direction}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
