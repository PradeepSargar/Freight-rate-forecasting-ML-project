"""
FreightIQ — Formatting Utilities
Number, percent, and date helpers used across the dashboard.
"""

from __future__ import annotations


def fmt_number(value: float | None, decimals: int = 2) -> str:
    """Format a number with commas and given decimal places."""
    if value is None:
        return "—"
    return f"{value:,.{decimals}f}"


def fmt_int(value: float | None) -> str:
    """Format as whole integer with commas."""
    if value is None:
        return "—"
    return f"{int(round(value)):,}"


def fmt_pct(value: float | None, decimals: int = 2) -> str:
    """Format a percentage value."""
    if value is None:
        return "—"
    sign = "+" if value > 0 else ""
    return f"{sign}{value:.{decimals}f}%"


def fmt_change(value: float | None, decimals: int = 2) -> str:
    """Format an absolute change value with sign."""
    if value is None:
        return "—"
    sign = "+" if value > 0 else ""
    return f"{sign}{value:,.{decimals}f}"


def direction_arrow(direction: str) -> str:
    """Return arrow symbol for direction."""
    mapping = {
        "Increasing": "↑",
        "Decreasing": "↓",
        "Neutral":    "→",
    }
    return mapping.get(direction, "—")


def direction_color(direction: str) -> str:
    """Return CSS color for direction."""
    mapping = {
        "Increasing": "#22C55E",
        "Decreasing": "#EF4444",
        "Neutral":    "#F59E0B",
    }
    return mapping.get(direction, "#94A3B8")


def horizon_label(horizon: str) -> str:
    """Convert '7 observations' to '7-Observation'."""
    parts = horizon.strip().split()
    if parts:
        return f"{parts[0]}-Observation"
    return horizon


def horizon_short(horizon: str) -> str:
    """'7 observations' → 'H7'"""
    parts = horizon.strip().split()
    return f"H{parts[0]}" if parts else horizon
