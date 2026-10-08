"""
FreightIQ — Data Loader
Handles all data loading with caching. Never retrain or reload unnecessarily.
"""

from __future__ import annotations

import os
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path


# ── Resolve absolute paths regardless of working directory ──────────────────
_HERE = Path(__file__).resolve().parent          # FreightIQ/utils/
_APP_ROOT = _HERE.parent                         # FreightIQ/
_PROJ_ROOT = _APP_ROOT.parent                    # project root

if (_APP_ROOT / "data" / "processed").exists():
    _PROCESSED = _APP_ROOT / "data" / "processed"
else:
    _PROCESSED = _PROJ_ROOT / "data" / "processed"

FORECASTS_CSV   = _PROCESSED / "model1_final_forecasts.csv"
CLEANED_CSV     = _PROCESSED / "model1_cleaned_dataset.csv"
FEATURE_ENG_CSV = _PROCESSED / "model1_feature_engineered.csv"


# ── Data loading helpers ─────────────────────────────────────────────────────

@st.cache_data(ttl=3600, show_spinner=False)
def load_forecasts() -> pd.DataFrame | None:
    """Load model1_final_forecasts.csv."""
    if not FORECASTS_CSV.exists():
        return None
    df = pd.read_csv(FORECASTS_CSV, parse_dates=["Forecast_Date"])
    return df


@st.cache_data(ttl=3600, show_spinner=False)
def load_cleaned_dataset() -> pd.DataFrame | None:
    """Load model1_cleaned_dataset.csv."""
    if not CLEANED_CSV.exists():
        return None
    df = pd.read_csv(CLEANED_CSV, parse_dates=["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    return df


@st.cache_data(ttl=3600, show_spinner=False)
def load_feature_engineered() -> pd.DataFrame | None:
    """Load model1_feature_engineered.csv."""
    if not FEATURE_ENG_CSV.exists():
        return None
    df = pd.read_csv(FEATURE_ENG_CSV, parse_dates=["Date"])
    df = df.sort_values("Date").reset_index(drop=True)
    return df


# ── Derived helpers ──────────────────────────────────────────────────────────

def get_forecast_for_horizon(df: pd.DataFrame, horizon_label: str) -> dict | None:
    """
    Return a dict with keys: current_bdi, forecasted_bdi, forecast_date, horizon
    for the given horizon_label (e.g. '7 observations').
    """
    if df is None:
        return None
    row = df[df["Forecast_Horizon"].str.lower() == horizon_label.lower()]
    if row.empty:
        return None
    row = row.iloc[0]
    current = float(row["Current_BDI"])
    forecast = float(row["Forecasted_BDI"])
    change = forecast - current
    pct_change = (change / current) * 100 if current != 0 else 0.0
    return {
        "current_bdi":     current,
        "forecasted_bdi":  forecast,
        "forecast_date":   row["Forecast_Date"],
        "horizon":         row["Forecast_Horizon"],
        "change":          change,
        "pct_change":      pct_change,
        "direction":       "Increasing" if change > 0 else ("Decreasing" if change < 0 else "Neutral"),
    }


def get_all_forecasts(df: pd.DataFrame) -> list[dict]:
    """Return list of forecast dicts for all horizons."""
    horizons = ["7 observations", "14 observations", "30 observations"]
    return [get_forecast_for_horizon(df, h) for h in horizons]


def get_current_bdi(df: pd.DataFrame | None) -> float | None:
    """Get Current_BDI from forecast CSV (single source of truth)."""
    if df is None or df.empty:
        return None
    return float(df.iloc[0]["Current_BDI"])


def get_forecast_date(df: pd.DataFrame | None) -> str | None:
    """Get Forecast_Date formatted nicely."""
    if df is None or df.empty:
        return None
    d = df.iloc[0]["Forecast_Date"]
    if pd.isnull(d):
        return None
    if hasattr(d, "strftime"):
        return d.strftime("%d %B %Y")
    return str(d)


def get_correlation_matrix(df: pd.DataFrame | None) -> pd.DataFrame | None:
    """Compute correlation matrix for the primary indicators."""
    if df is None:
        return None
    cols = [c for c in ["BDI", "BCI", "BPI", "BSI", "Brent", "USD_INR", "Coal", "Iron_Ore"] if c in df.columns]
    if len(cols) < 2:
        return None
    return df[cols].corr()
