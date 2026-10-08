"""
FreightIQ — Charts Component
All Plotly chart builders. Pure functions; no Streamlit calls.
"""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots


# ── Color palette ────────────────────────────────────────────────────────────
C_BG        = "#0B1120"
C_CARD      = "#151E2E"
C_PAPER     = "#111827"
C_GRID      = "#1E2940"
C_TEXT      = "#F8FAFC"
C_TEXT2     = "#94A3B8"
C_MUTED     = "#64748B"
C_ACCENT    = "#38BDF8"
C_GREEN     = "#22C55E"
C_YELLOW    = "#F59E0B"
C_RED       = "#EF4444"

HORIZON_COLORS = {
    "7 observations":  "#38BDF8",
    "14 observations": "#22C55E",
    "30 observations": "#F59E0B",
}

HORIZON_LABELS = {
    "7 observations":  "7-Obs",
    "14 observations": "14-Obs",
    "30 observations": "30-Obs",
}

_LAYOUT_DEFAULTS = dict(
    paper_bgcolor=C_PAPER,
    plot_bgcolor=C_CARD,
    font=dict(family="Inter, Segoe UI, sans-serif", color=C_TEXT2, size=12),
    margin=dict(l=20, r=20, t=50, b=20),
    legend=dict(
        bgcolor=C_PAPER,
        bordercolor=C_GRID,
        borderwidth=1,
        font=dict(color=C_TEXT2, size=11),
    ),
    xaxis=dict(
        gridcolor=C_GRID,
        showgrid=True,
        zeroline=False,
        tickfont=dict(color=C_TEXT2),
        linecolor=C_GRID,
    ),
    yaxis=dict(
        gridcolor=C_GRID,
        showgrid=True,
        zeroline=False,
        tickfont=dict(color=C_TEXT2),
        linecolor=C_GRID,
    ),
    hoverlabel=dict(
        bgcolor=C_CARD,
        bordercolor=C_GRID,
        font=dict(color=C_TEXT, size=12),
    ),
)

_RANGE_BUTTONS = [
    dict(count=6,  label="6M",  step="month", stepmode="backward"),
    dict(count=1,  label="1Y",  step="year",  stepmode="backward"),
    dict(count=3,  label="3Y",  step="year",  stepmode="backward"),
    dict(count=5,  label="5Y",  step="year",  stepmode="backward"),
    dict(step="all", label="All"),
]


def _apply_defaults(fig: go.Figure, title: str = "") -> go.Figure:
    fig.update_layout(**_LAYOUT_DEFAULTS)
    if title:
        fig.update_layout(
            title=dict(
                text=title,
                font=dict(color=C_TEXT, size=14, family="Inter, Segoe UI, sans-serif"),
                x=0,
                xanchor="left",
                pad=dict(l=4),
            )
        )
    fig.update_xaxes(
        rangeselector=dict(
            buttons=_RANGE_BUTTONS,
            bgcolor=C_PAPER,
            activecolor=C_ACCENT,
            bordercolor=C_GRID,
            font=dict(color=C_TEXT2, size=11),
        ),
        rangeslider=dict(visible=False),
    )
    return fig


# ── Main BDI historical + forecast chart ─────────────────────────────────────

def build_bdi_forecast_chart(
    hist_df: pd.DataFrame,
    forecasts: list[dict | None],
    title: str = "BDI Historical Trend & Forecast",
    selected_horizon: int | None = None,
) -> go.Figure:
    """
    Large interactive chart: historical BDI line + scatter forecast points.
    hist_df must have columns: Date, BDI.
    forecasts: list of forecast dicts from data_loader.
    selected_horizon: active forecast horizon (7, 14, or 30) to visually highlight.
    """
    if selected_horizon is None:
        try:
            import streamlit as st
            selected_horizon = st.session_state.get("forecast_horizon", 7)
        except Exception:
            selected_horizon = 7

    fig = go.Figure()

    if hist_df is not None and not hist_df.empty:
        hist_df = hist_df.sort_values("Date")
        # Historical line
        fig.add_trace(
            go.Scatter(
                x=hist_df["Date"],
                y=hist_df["BDI"],
                mode="lines",
                name="Historical BDI",
                line=dict(color=C_TEXT2, width=1.5),
                hovertemplate="<b>%{x|%d %b %Y}</b><br>BDI: <b>%{y:,.0f}</b><extra></extra>",
            )
        )
        # Current BDI marker (last historical point)
        last_row = hist_df.iloc[-1]
        fig.add_trace(
            go.Scatter(
                x=[last_row["Date"]],
                y=[last_row["BDI"]],
                mode="markers",
                name="Current BDI",
                marker=dict(color=C_TEXT, size=8, symbol="circle",
                            line=dict(color=C_ACCENT, width=2)),
                hovertemplate="<b>Current BDI</b><br>%{x|%d %b %Y}<br>BDI: <b>%{y:,.0f}</b><extra></extra>",
            )
        )

    # Forecast scatter points
    for fc in forecasts:
        if fc is None:
            continue
        h = fc["horizon"]
        h_days = fc.get("horizon_days") or int("".join(filter(str.isdigit, str(h))) or 0)
        is_selected = (h_days == selected_horizon)
        color = HORIZON_COLORS.get(h, C_ACCENT)
        label = HORIZON_LABELS.get(h, h)

        if is_selected:
            marker_size = 15
            marker_line = dict(color="#FFFFFF", width=2.5)
            text_str = f"  <b>★ {label}: {fc['forecasted_bdi']:,.0f} (Active)</b>"
            text_font = dict(color=color, size=11)
            name_str = f"Forecast {label} (Active)"
        else:
            marker_size = 9
            marker_line = dict(color=C_PAPER, width=1)
            text_str = f"  {label}: {fc['forecasted_bdi']:,.0f}"
            text_font = dict(color=color, size=9)
            name_str = f"Forecast {label}"

        fig.add_trace(
            go.Scatter(
                x=[fc["forecast_date"]],
                y=[fc["forecasted_bdi"]],
                mode="markers+text",
                name=name_str,
                marker=dict(
                    color=color,
                    size=marker_size,
                    symbol="diamond",
                    line=marker_line,
                ),
                text=[text_str],
                textposition="middle right",
                textfont=text_font,
                hovertemplate=(
                    f"<b>{label} Forecast {'[Active Horizon]' if is_selected else ''}</b><br>"
                    "Date: <b>%{x|%d %b %Y}</b><br>"
                    "BDI: <b>%{y:,.2f}</b><extra></extra>"
                ),
            )
        )

        # Highlight projection line from last historical BDI to the active forecast point
        if is_selected and hist_df is not None and not hist_df.empty:
            last_row = hist_df.iloc[-1]
            fig.add_trace(
                go.Scatter(
                    x=[last_row["Date"], fc["forecast_date"]],
                    y=[last_row["BDI"], fc["forecasted_bdi"]],
                    mode="lines",
                    name=f"{label} Trend Projection",
                    line=dict(color=color, width=2, dash="dash"),
                    hoverinfo="skip",
                )
            )

    # Forecast zone shading
    if hist_df is not None and not hist_df.empty:
        last_date = hist_df["Date"].max()
        fig.add_vrect(
            x0=last_date,
            x1=last_date + pd.Timedelta(days=45),
            fillcolor=C_ACCENT,
            opacity=0.04,
            line_width=0,
            annotation_text="Forecast Zone",
            annotation_position="top left",
            annotation=dict(font=dict(color=C_MUTED, size=10)),
        )

    fig = _apply_defaults(fig, title)
    fig.update_layout(height=420, showlegend=True)
    return fig


# ── Single-horizon forecast chart ────────────────────────────────────────────

def build_horizon_chart(
    hist_df: pd.DataFrame,
    fc: dict | None,
    horizon_label: str,
) -> go.Figure:
    """Focused chart for a single forecast horizon."""
    fig = go.Figure()
    if hist_df is not None and not hist_df.empty:
        hist_df = hist_df.sort_values("Date")
        recent = hist_df.tail(180)  # ~6 months for readability
        fig.add_trace(
            go.Scatter(
                x=recent["Date"], y=recent["BDI"],
                mode="lines", name="Historical BDI",
                line=dict(color=C_TEXT2, width=1.5),
                hovertemplate="<b>%{x|%d %b %Y}</b><br>BDI: <b>%{y:,.0f}</b><extra></extra>",
            )
        )

    if fc is not None:
        color = HORIZON_COLORS.get(horizon_label, C_ACCENT)
        fig.add_trace(
            go.Scatter(
                x=[fc["forecast_date"]], y=[fc["forecasted_bdi"]],
                mode="markers+text",
                name=f"Forecast ({HORIZON_LABELS.get(horizon_label, '')})",
                marker=dict(color=color, size=14, symbol="diamond",
                            line=dict(color=C_PAPER, width=2)),
                text=[f"  {fc['forecasted_bdi']:,.2f}"],
                textposition="middle right",
                textfont=dict(color=color, size=11),
                hovertemplate=(
                    "<b>Forecast</b><br>"
                    "Date: <b>%{x|%d %b %Y}</b><br>"
                    "BDI: <b>%{y:,.2f}</b><extra></extra>"
                ),
            )
        )

    fig = _apply_defaults(fig, f"BDI Trend — {HORIZON_LABELS.get(horizon_label, horizon_label)} Forecast")
    fig.update_layout(height=380)
    return fig


# ── Indicator time-series charts ─────────────────────────────────────────────

def _hex_to_rgba(hex_color: str, alpha: float = 0.08) -> str:
    hex_color = hex_color.lstrip("#")
    if len(hex_color) == 6:
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        return f"rgba({r}, {g}, {b}, {alpha})"
    return f"rgba(56, 189, 248, {alpha})"


def build_indicator_chart(
    df: pd.DataFrame,
    col: str,
    title: str,
    color: str = C_ACCENT,
    height: int = 280,
    show_range_selector: bool = True,
) -> go.Figure | None:
    if df is None or col not in df.columns:
        return None
    df = df.sort_values("Date")
    fig = go.Figure()
    fill_rgba = _hex_to_rgba(color, 0.08) if color.startswith("#") else color
    fig.add_trace(
        go.Scatter(
            x=df["Date"], y=df[col],
            mode="lines",
            name=title,
            line=dict(color=color, width=1.5),
            fill="tozeroy",
            fillcolor=fill_rgba,
            hovertemplate=f"<b>%{{x|%d %b %Y}}</b><br>{title}: <b>%{{y:,.2f}}</b><extra></extra>",
        )
    )
    fig = _apply_defaults(fig, title)
    fig.update_layout(height=height, showlegend=False)
    if not show_range_selector:
        fig.update_xaxes(rangeselector=None)
    return fig


def build_multi_indicator_chart(
    df: pd.DataFrame,
    cols: list[str],
    title: str,
    height: int = 320,
) -> go.Figure | None:
    if df is None:
        return None
    palette = [C_ACCENT, C_GREEN, C_YELLOW, C_RED, "#A78BFA", "#FB923C", "#34D399", "#F472B6"]
    df = df.sort_values("Date")
    fig = go.Figure()
    for i, col in enumerate(cols):
        if col not in df.columns:
            continue
        color = palette[i % len(palette)]
        fig.add_trace(
            go.Scatter(
                x=df["Date"], y=df[col],
                mode="lines", name=col,
                line=dict(color=color, width=1.5),
                hovertemplate=f"<b>%{{x|%d %b %Y}}</b><br>{col}: <b>%{{y:,.2f}}</b><extra></extra>",
            )
        )
    fig = _apply_defaults(fig, title)
    fig.update_layout(height=height)
    return fig


# ── Correlation heatmap ───────────────────────────────────────────────────────

def build_correlation_heatmap(corr_df: pd.DataFrame | None) -> go.Figure | None:
    if corr_df is None or corr_df.empty:
        return None

    labels = list(corr_df.columns)
    z = corr_df.values.round(2).tolist()

    # Build custom text matrix
    text = [[f"{v:.2f}" for v in row] for row in corr_df.values]

    colorscale = [
        [0.0,  "#EF4444"],
        [0.35, "#7A2020"],
        [0.5,  "#1E2940"],
        [0.65, "#0F4A7A"],
        [1.0,  "#38BDF8"],
    ]

    fig = go.Figure(
        go.Heatmap(
            z=z,
            x=labels,
            y=labels,
            text=text,
            texttemplate="%{text}",
            colorscale=colorscale,
            zmin=-1, zmax=1,
            showscale=True,
            colorbar=dict(
                tickfont=dict(color=C_TEXT2),
                outlinecolor=C_GRID,
                bgcolor=C_PAPER,
                title=dict(text="r", font=dict(color=C_TEXT2)),
            ),
            hovertemplate="<b>%{y} ↔ %{x}</b><br>Correlation: <b>%{z:.2f}</b><extra></extra>",
            textfont=dict(color=C_TEXT, size=11),
        )
    )
    fig.update_layout(**_LAYOUT_DEFAULTS)
    fig.update_layout(
        title=dict(
            text="Correlation Matrix — Freight & Economic Indicators",
            font=dict(color=C_TEXT, size=14),
            x=0, xanchor="left",
        ),
        height=400,
    )
    fig.update_xaxes(tickfont=dict(color=C_TEXT2), side="bottom", showgrid=False)
    fig.update_yaxes(tickfont=dict(color=C_TEXT2), autorange="reversed", showgrid=False)
    return fig


# ── Feature importance chart ──────────────────────────────────────────────────

def build_feature_importance_chart(
    fi: dict,
    top_n: int = 15,
    title: str = "Top Freight Forecasting Features",
) -> go.Figure | None:
    if not fi:
        return None
    sorted_fi = sorted(fi.items(), key=lambda x: x[1], reverse=True)[:top_n]
    names = [x[0] for x in reversed(sorted_fi)]
    values = [x[1] for x in reversed(sorted_fi)]

    # Color gradient: top features get accent, others muted
    max_v = max(values) if values else 1
    colors = [
        C_ACCENT if v / max_v > 0.5 else (C_GREEN if v / max_v > 0.25 else C_MUTED)
        for v in values
    ]

    fig = go.Figure(
        go.Bar(
            x=values, y=names,
            orientation="h",
            marker=dict(color=colors, opacity=0.9),
            hovertemplate="<b>%{y}</b><br>Importance: <b>%{x:.4f}</b><extra></extra>",
        )
    )
    fig.update_layout(**_LAYOUT_DEFAULTS)
    fig.update_layout(
        title=dict(text=title, font=dict(color=C_TEXT, size=14), x=0, xanchor="left"),
        height=max(350, top_n * 26),
        showlegend=False,
    )
    fig.update_yaxes(tickfont=dict(color=C_TEXT2, size=11), showgrid=False)
    fig.update_xaxes(title=dict(text="Importance Score"), tickfont=dict(color=C_TEXT2), gridcolor=C_GRID)
    return fig


# ── Performance bar chart ─────────────────────────────────────────────────────

def build_performance_chart(perf_rows: list[dict]) -> go.Figure | None:
    if not perf_rows:
        return None
    import pandas as pd
    df = pd.DataFrame(perf_rows)

    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=["MAE", "RMSE", "MAPE (%)"],
    )
    horizon_palette = {
        "7 Obs":  C_ACCENT,
        "14 Obs": C_GREEN,
        "30 Obs": C_YELLOW,
    }
    val_dash = {"Holdout": "solid", "TimeSeriesSplit": "dash"}

    for idx, metric in enumerate(["MAE", "RMSE", "MAPE (%)"]):
        for horizon_key, color in horizon_palette.items():
            for val_type, dash in val_dash.items():
                subset = df[(df["Horizon"] == horizon_key) & (df["Validation"] == val_type)]
                if subset.empty:
                    continue
                val = subset[metric].values[0]
                fig.add_trace(
                    go.Bar(
                        x=[f"{horizon_key}<br>{val_type}"],
                        y=[val],
                        name=f"{horizon_key} {val_type}",
                        marker_color=color,
                        opacity=0.9 if val_type == "Holdout" else 0.55,
                        showlegend=(idx == 0),
                        hovertemplate=f"<b>{horizon_key} — {val_type}</b><br>{metric}: <b>%{{y:.2f}}</b><extra></extra>",
                    ),
                    row=1, col=idx + 1,
                )

    fig.update_layout(
        **_LAYOUT_DEFAULTS,
        height=360,
        barmode="group",
        title=dict(
            text="Validation Performance by Horizon",
            font=dict(color=C_TEXT, size=14),
            x=0, xanchor="left",
        ),
    )
    # Style subplot titles
    for ann in fig.layout.annotations:
        ann.font.color = C_TEXT2
    return fig
