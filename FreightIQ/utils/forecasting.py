"""
FreightIQ — Forecasting Utilities
Model loading and inference helpers. Uses st.cache_resource for model artifacts.
"""

from __future__ import annotations

import streamlit as st
from pathlib import Path

# Model path
_HERE = Path(__file__).resolve().parent
_APP_ROOT = _HERE.parent
_PROJ_ROOT = _APP_ROOT.parent

if (_APP_ROOT / "models" / "forecasting").exists():
    _MODELS_DIR = _APP_ROOT / "models" / "forecasting"
else:
    _MODELS_DIR = _PROJ_ROOT / "models" / "forecasting"


HORIZON_METRICS = {
    "7 observations": {
        "holdout": {"MAE": 224.61, "RMSE": 292.70, "MAPE": 15.49},
        "tss":     {"MAE": 366.08, "RMSE": 471.45, "MAPE": 27.78},
    },
    "14 observations": {
        "holdout": {"MAE": 284.28, "RMSE": 375.00, "MAPE": 20.31},
        "tss":     {"MAE": 474.80, "RMSE": 592.45, "MAPE": 36.96},
    },
    "30 observations": {
        "holdout": {"MAE": 322.77, "RMSE": 401.46, "MAPE": 26.40},
        "tss":     {"MAE": 491.56, "RMSE": 610.22, "MAPE": 34.91},
    },
}


@st.cache_resource(show_spinner=False)
def load_xgboost_model(horizon_label: str):
    """
    Attempt to load a saved XGBoost model for the given horizon.
    Returns the model if available, None otherwise.
    Models are expected at models/forecasting/xgb_{n}obs.json or .pkl
    """
    try:
        import xgboost as xgb
        n = horizon_label.split()[0]
        candidates = [
            _MODELS_DIR / f"xgb_{n}obs.json",
            _MODELS_DIR / f"xgb_{n}obs.ubj",
            _MODELS_DIR / f"xgb_h{n}.json",
            _MODELS_DIR / f"model_{n}.json",
        ]
        for path in candidates:
            if path.exists():
                model = xgb.XGBRegressor()
                model.load_model(str(path))
                return model
        # pkl fallback
        import pickle
        pkl_candidates = [
            _MODELS_DIR / f"xgb_{n}obs.pkl",
            _MODELS_DIR / f"model_{n}.pkl",
        ]
        for path in pkl_candidates:
            if path.exists():
                with open(path, "rb") as f:
                    return pickle.load(f)
    except Exception:
        pass
    return None


def get_feature_importance(horizon_label: str) -> dict | None:
    """
    Return feature importance dict {feature_name: importance_score} for a horizon.
    Returns None if model is not available.
    """
    model = load_xgboost_model(horizon_label)
    if model is None:
        return None
    try:
        fi = model.get_booster().get_fscore()
        if not fi:
            fi = dict(zip(model.feature_names_in_, model.feature_importances_))
        return fi
    except Exception:
        try:
            fi = dict(zip(model.feature_names_in_, model.feature_importances_))
            return fi
        except Exception:
            return None


def get_performance_table() -> list[dict]:
    """Return list of performance dicts for all horizons and validation types."""
    rows = []
    for horizon, metrics in HORIZON_METRICS.items():
        n = horizon.split()[0]
        rows.append({
            "Horizon": f"{n} Obs",
            "Validation": "Holdout",
            "MAE": metrics["holdout"]["MAE"],
            "RMSE": metrics["holdout"]["RMSE"],
            "MAPE (%)": metrics["holdout"]["MAPE"],
        })
        rows.append({
            "Horizon": f"{n} Obs",
            "Validation": "TimeSeriesSplit",
            "MAE": metrics["tss"]["MAE"],
            "RMSE": metrics["tss"]["RMSE"],
            "MAPE (%)": metrics["tss"]["MAPE"],
        })
    return rows
