"""
FreightIQ — Market Insights Component
Generates dynamic AI-style market commentary based on forecast data.
"""

from __future__ import annotations

import streamlit as st
from utils.formatting import fmt_number, fmt_pct, direction_arrow


def _direction_word(direction: str) -> str:
    return {
        "Increasing": "upward",
        "Decreasing": "downward",
        "Neutral": "lateral",
    }.get(direction, "mixed")


def _strength_word(pct: float) -> str:
    if abs(pct) < 5:
        return "modest"
    elif abs(pct) < 15:
        return "moderate"
    elif abs(pct) < 30:
        return "notable"
    else:
        return "significant"


def generate_market_insight(
    current_bdi: float | None,
    forecasts: list[dict | None],
) -> str:
    """Generate a dynamic, hedge-appropriate market commentary paragraph."""
    if current_bdi is None:
        return "Forecast data is currently unavailable. Please verify data files."

    h7, h14, h30 = (forecasts + [None, None, None])[:3]

    # Determine overall trajectory
    directions = [fc["direction"] for fc in [h7, h14, h30] if fc is not None]
    upcount = directions.count("Increasing")
    dncount = directions.count("Decreasing")

    if upcount == 3:
        trajectory = "an upward trajectory across all three forecast horizons"
        implication = "suggesting a potential strengthening of dry-bulk freight-market conditions"
    elif dncount == 3:
        trajectory = "a downward trajectory across all three forecast horizons"
        implication = "suggesting a potential softening in dry-bulk freight-market demand"
    elif upcount > dncount:
        trajectory = "a predominantly upward trajectory"
        implication = "suggesting tentative improvement in market conditions, though uncertainty persists across longer horizons"
    elif dncount > upcount:
        trajectory = "a predominantly downward trajectory"
        implication = "suggesting potential near-term market weakness"
    else:
        trajectory = "a mixed directional signal across forecast horizons"
        implication = "indicating elevated market uncertainty and directional ambiguity"

    # Build body
    parts = [
        f"FreightIQ currently observes a Baltic Dry Index (BDI) of "
        f"<strong>{fmt_number(current_bdi, 0)}</strong>. "
        f"The XGBoost model forecasts {trajectory}, {implication}."
    ]

    if h7 is not None:
        strength = _strength_word(h7["pct_change"])
        parts.append(
            f"Over the short term (7 observations), the model suggests a {strength} "
            f"{_direction_word(h7['direction'])} movement to a forecasted BDI of "
            f"<strong>{fmt_number(h7['forecasted_bdi'], 2)}</strong> "
            f"({fmt_pct(h7['pct_change'], 2)})."
        )

    if h14 is not None:
        strength = _strength_word(h14["pct_change"])
        parts.append(
            f"At the medium-term horizon (14 observations), the model estimates a {strength} "
            f"{_direction_word(h14['direction'])} trend toward "
            f"<strong>{fmt_number(h14['forecasted_bdi'], 2)}</strong> "
            f"({fmt_pct(h14['pct_change'], 2)})."
        )

    if h30 is not None:
        strength = _strength_word(h30["pct_change"])
        parts.append(
            f"Over the longer horizon (30 observations), the model projects a {strength} "
            f"{_direction_word(h30['direction'])} potential, with a forecasted BDI of "
            f"<strong>{fmt_number(h30['forecasted_bdi'], 2)}</strong> "
            f"({fmt_pct(h30['pct_change'], 2)})."
        )

    parts.append(
        "These estimates are model-based statistical projections. "
        "Actual freight-market conditions may deviate significantly from modeled forecasts "
        "due to geopolitical, macroeconomic, or supply-demand shocks not captured in historical data."
    )

    return " ".join(parts)


def render_market_insight(
    current_bdi: float | None,
    forecasts: list[dict | None],
) -> None:
    """Render the market insight section."""
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:8px; margin-bottom:0.5rem;">
            <span style="font-size:0.68rem; color:#38BDF8; font-weight:700;
                         text-transform:uppercase; letter-spacing:0.1em;">
                AI-Assisted Market Insight
            </span>
            <span style="font-size:0.65rem; color:#64748B; border:1px solid #1E2940;
                         border-radius:3px; padding:1px 5px;">Model-Based</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    insight_text = generate_market_insight(current_bdi, forecasts)
    st.markdown(
        f'<div class="fiq-insight-box">{insight_text}</div>',
        unsafe_allow_html=True,
    )
