# NGO Turnover Analysis Tool

A lightweight, user-friendly tool for HR managers at non-profits to analyze employee turnover patterns, calculate costs, and identify early warning signs.

## Features

- **Easy Data Import**: Upload Excel spreadsheets with employee data
- **Cohort Analysis**: Track retention by hire cohort, department, role
- **Cost Calculator**: Estimate true turnover costs (recruitment + training + productivity loss)
- **Visual Dashboards**: Interactive charts showing trends over time
- **Predictive Insights**: Flag potential at-risk employees
- **Benchmark Comparisons**: Compare against sector averages

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

Open your browser to `http://localhost:8501`

## Data Requirements

Your Excel file should have these columns (minimum):
- `employee_id`: Unique identifier
- `name`: Employee name
- `hire_date`: Start date (YYYY-MM-DD)
- `termination_date`: End date (YYYY-MM-DD, blank if still employed)
- `department`: Department/team name
- `role`: Job title or role category

Optional but recommended:
- `termination_reason`: Voluntary/Involuntary/Retirement
- `salary`: Annual compensation
- `performance_rating`: Most recent rating

A sample template is provided in `data/sample_data.xlsx`

## Methodology

**Cohort Analysis**: Groups employees by hire period and tracks retention rates over time. Shows what percentage remain after 3, 6, 12, 24 months.

**Cost Calculation**: Based on SHRM research:
- Recruitment costs: ~20% of annual salary
- Training costs: ~10% of annual salary
- Productivity loss: ~50% of annual salary (6-month ramp time)
- Total: ~80% of annual salary per turnover

**Predictive Flags**: Uses patterns from historical data:
- Tenure patterns (highest risk periods)
- Department trends
- Seasonal variations

## Use Cases

- **Board Reports**: Generate quarterly turnover metrics
- **Budget Planning**: Forecast turnover costs for FY planning
- **Intervention**: Identify high-risk periods for retention efforts
- **Benchmarking**: Compare your org to sector standards

## Tech Stack

- Python 3.9+
- Pandas for data processing
- Streamlit for interactive UI
- Plotly for visualizations
- Scikit-learn for predictive models

## Project Structure

```
turnover-analysis/
├── app.py                  # Main Streamlit application
├── src/
│   ├── data_loader.py      # Excel import & validation
│   ├── cohort_analysis.py  # Retention calculations
│   ├── cost_calculator.py  # Financial impact modeling
│   ├── visualizations.py   # Chart generation
│   └── predictive.py       # Risk flagging logic
└── data/
    └── sample_data.xlsx    # Template file
```

## Privacy Note

This tool runs locally on your machine. No data is uploaded to external servers. All analysis happens in your browser.

## Future Enhancements

- Export reports to PDF
- Integration with common HRIS systems (BambooHR, Gusto, Rippling)
- More sophisticated ML models for prediction
- Diversity/equity metrics by demographic groups

## License

MIT License - Free to use and modify

## Author

Built by someone who's wrestled with NGO HR data and wanted a better way.
