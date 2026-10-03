# Architecture

FreightIQ separates the workflow into data collection and preparation, model
training, evaluation, inference, and a Streamlit dashboard.

- `src/data/` contains collectors and preprocessing/feature-engineering modules.
- `src/models/` contains forecasting and vessel-selection model implementations.
- `src/evaluation/` contains task-specific metrics.
- `src/inference/` exposes trained models to application code.
- `dashboard/` contains the dashboard entry point, pages, and reusable UI pieces.

Raw inputs live in `data/raw/`; generated datasets and model artifacts live in
`data/processed/` and `models/`, respectively. Model artifact files are created
by training workflows and are intentionally not empty placeholders.