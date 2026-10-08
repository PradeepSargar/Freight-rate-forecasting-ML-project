"""
FreightIQ — KPI Cards Component
Renders professional metric cards for BDI, forecasts, and direction.
"""

from __future__ import annotations

import textwrap
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
    selected_horizon: int | None = None,
) -> None:
    """
    Render the 5 KPI cards corresponding to the selected forecast horizon:
      Current BDI | {selected_horizon}-Observation Forecast | Change | Percentage Change | Direction
    """
    if selected_horizon is None:
        selected_horizon = st.session_state.get("forecast_horizon", 7)

    # Find the forecast matching selected_horizon
    selected_fc = None
    for fc in forecasts:
        if fc is not None:
            h_days = fc.get("horizon_days") or int("".join(filter(str.isdigit, str(fc.get("horizon", "")))) or 0)
            if h_days == selected_horizon:
                selected_fc = fc
                break

    if selected_fc is None and forecasts and forecasts[0] is not None:
        selected_fc = forecasts[0]

    cols = st.columns(5, gap="small")

    # ── Card 0: Current BDI ─────────────────────────────────────────────────
    with cols[0]:
        bdi_val = fmt_number(current_bdi, 0) if current_bdi is not None else "—"
        date_sub = forecast_date or "—"
        st.markdown(
            textwrap.dedent(f"""
            <div class="fiq-card" style="height:130px;">
                <div class="fiq-label">Current BDI</div>
                <div class="fiq-value">{bdi_val}</div>
                <div class="fiq-muted" style="margin-top:0.4rem;">As of {date_sub}</div>
            </div>
            """).strip(),
            unsafe_allow_html=True,
        )

    # ── Card 1: {selected_horizon}-Observation Forecast ──────────────────────
    with cols[1]:
        if selected_fc is None:
            fc_val = "—"
            sub_text = "Data unavailable"
        else:
            fc_val = fmt_number(selected_fc["forecasted_bdi"], 2)
            sub_text = f"<span class='fiq-badge' style='font-size:0.65rem;'>{selected_horizon} Observations</span>"
        st.markdown(
            textwrap.dedent(f"""
            <div class="fiq-card" style="height:130px;">
                <div class="fiq-label">{selected_horizon}-Observation Forecast</div>
                <div class="fiq-value">{fc_val}</div>
                <div style="margin-top:0.4rem;">{sub_text}</div>
            </div>
            """).strip(),
            unsafe_allow_html=True,
        )

    # ── Card 2: Change ──────────────────────────────────────────────────────
    with cols[2]:
        if selected_fc is None:
            chg_val = "—"
            color = "#94A3B8"
        else:
            chg_val = fmt_change(selected_fc["change"], 2)
            color = "#22C55E" if selected_fc["change"] > 0 else ("#EF4444" if selected_fc["change"] < 0 else "#F59E0B")
        st.markdown(
            textwrap.dedent(f"""
            <div class="fiq-card" style="height:130px;">
                <div class="fiq-label">Change</div>
                <div class="fiq-value" style="color:{color};">{chg_val}</div>
                <div class="fiq-muted" style="margin-top:0.4rem;">vs Current BDI</div>
            </div>
            """).strip(),
            unsafe_allow_html=True,
        )

    # ── Card 3: Percentage Change ───────────────────────────────────────────
    with cols[3]:
        if selected_fc is None:
            pct_val = "—"
            color = "#94A3B8"
        else:
            pct_val = fmt_pct(selected_fc["pct_change"], 2)
            color = "#22C55E" if selected_fc["pct_change"] > 0 else ("#EF4444" if selected_fc["pct_change"] < 0 else "#F59E0B")
        st.markdown(
            textwrap.dedent(f"""
            <div class="fiq-card" style="height:130px;">
                <div class="fiq-label">Percentage Change</div>
                <div class="fiq-value" style="color:{color};">{pct_val}</div>
                <div class="fiq-muted" style="margin-top:0.4rem;">Expected Growth</div>
            </div>
            """).strip(),
            unsafe_allow_html=True,
        )

    # ── Card 4: Direction ───────────────────────────────────────────────────
    with cols[4]:
        if selected_fc is not None:
            direction = selected_fc["direction"]
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
            textwrap.dedent(f"""
            <div class="fiq-card" style="height:130px;">
                <div class="fiq-label">Direction</div>
                <div style="font-size:1.9rem; font-weight:800; color:{color};
                            line-height:1.2; margin-top:0.2rem;">{arrow}</div>
                <div style="margin-top:0.4rem;">
                    <span class="fiq-badge {badge_cls}">{direction}</span>
                </div>
            </div>
            """).strip(),
            unsafe_allow_html=True,
        )
