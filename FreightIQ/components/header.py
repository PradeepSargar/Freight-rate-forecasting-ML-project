"""
FreightIQ — Header Component
Renders page-level hero headers with branding.
"""

from __future__ import annotations
import streamlit as st


def render_hero(
    title: str,
    subtitle: str,
    badge_text: str | None = None,
    meta_items: list[tuple[str, str]] | None = None,
) -> None:
    """
    Render a full-width hero header block.
    meta_items: list of (label, value) pairs for metadata row.
    """
    badge_html = ""
    if badge_text:
        badge_html = f'<span class="fiq-badge" style="margin-bottom:0.75rem; display:inline-block;">{badge_text}</span><br>'

    meta_html = ""
    if meta_items:
        items_html = "".join(
            f'<div style="display:flex; flex-direction:column; gap:2px;">'
            f'<div style="font-size:0.65rem; color:#64748B; text-transform:uppercase; '
            f'letter-spacing:0.08em;">{label}</div>'
            f'<div style="font-size:0.78rem; color:#94A3B8; font-weight:500;">{value}</div>'
            f'</div>'
            for label, value in meta_items
        )
        meta_html = f"""
        <div style="display:flex; gap:2rem; margin-top:1rem; padding-top:1rem;
                    border-top:1px solid #1E2940;">
            {items_html}
        </div>
        """

    st.markdown(
        f"""
        <div style="padding: 1.5rem 0 1.25rem 0; border-bottom:1px solid #1E2940; margin-bottom:1.5rem;">
            {badge_html}
            <h1 style="font-size:1.75rem; font-weight:800; color:#F8FAFC; margin:0;
                       letter-spacing:0.02em; line-height:1.2;">{title}</h1>
            <p style="font-size:0.9rem; color:#64748B; margin:0.4rem 0 0 0;
                      font-weight:400; line-height:1.5;">{subtitle}</p>
            {meta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(title: str, subtitle: str = "") -> None:
    """Render a smaller in-page section header."""
    sub_html = (
        f'<p style="font-size:0.8rem; color:#64748B; margin:0.2rem 0 0 0;">{subtitle}</p>'
        if subtitle else ""
    )
    st.markdown(
        f"""
        <div style="margin:1.5rem 0 0.75rem 0;">
            <h3 style="font-size:1.05rem; font-weight:700; color:#F8FAFC; margin:0;">{title}</h3>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_disclaimer() -> None:
    """Render the standard FreightIQ model disclaimer."""
    st.markdown(
        """
        <div class="fiq-disclaimer">
            <strong style="color:#94A3B8; font-size:0.78rem;">⚠ Analytical Disclaimer</strong><br>
            FreightIQ provides model-based analytical forecasts for research and decision-support purposes.
            Forecasts represent statistical estimates and should not be interpreted as guaranteed future
            freight rates or financial advice.<br><br>
            The 7, 14 and 30 horizons represent future observations in the modeling dataset and
            should not automatically be interpreted as exact calendar-day forecasts.
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    """Render the professional FreightIQ footer."""
    st.markdown(
        """
        <div class="fiq-footer">
            <div style="font-size:0.82rem; font-weight:800; color:#94A3B8;
                        letter-spacing:0.1em;">FREIGHTIQ</div>
            <div style="color:#64748B; margin-top:2px;">
                Intelligent Freight Market Forecasting System
            </div>
            <div style="color:#1E2940; margin-top:6px; font-size:0.68rem;">
                Machine Learning &nbsp;•&nbsp; Freight Analytics &nbsp;•&nbsp; Decision Support
            </div>
            <div style="margin-top:6px; font-size:0.68rem; color:#1E2940;">
                XGBoost Regression &nbsp;|&nbsp; 7 / 14 / 30 Observation Forecasting
            </div>
            <div style="margin-top:6px; color:#1E2940;">&copy; 2026 FreightIQ</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
