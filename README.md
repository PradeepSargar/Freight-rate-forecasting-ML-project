# FreightIQ

FreightIQ is a project scaffold for freight-rate forecasting and vessel selection.

## Project layout

- `data/raw/`: source market, freight-index, and reference data.
- `data/processed/`: model-ready datasets.
- `notebooks/`: data collection, exploration, modeling, and evaluation workflows.
- `src/`: data processing, models, evaluation, inference, and utility modules.
- `models/`: trained model artifacts (generated during model training; not included yet).
- `dashboard/`: Streamlit dashboard pages, components, and theme.
- `config/`: project configuration.
- `tests/`: automated tests.
- `docs/` and `reports/`: project documentation and generated results.

## Setup

Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

The files in this scaffold are starting points; datasets and trained model
artifacts must be collected or generated before running the forecasting workflow.
