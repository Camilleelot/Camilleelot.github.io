# NGO Turnover Analysis Tool

A lightweight, user-friendly tool for HR managers at non-profits to analyze employee turnover patterns, calculate costs, and identify early warning signs.

## Features

- **Easy Data Import**: Upload Excel spreadsheets with employee data
- **Cohort Analysis**: Track retention by hire cohort, department, role
- **Case-Based Analysis**: Categorize terminations by tenure windows (0-3mo, 3-12mo, 1-3yr, etc.)
- **Sankey Flow Diagrams**: Visualize Department → Role → Outcome flows
- **Cost Calculator**: Estimate true turnover costs (recruitment + training + productivity loss)
- **Visual Dashboards**: Interactive charts showing trends over time
- **Predictive Insights**: Flag potential at-risk employees
- **Voluntary/Involuntary Tracking**: Separate analysis of voluntary vs involuntary exits
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
- `termination_reason`: Voluntary/Involuntary/Retirement (enables case-based analysis)
- `salary`: Annual compensation (needed for cost calculations)
- `employment_type`: Full-time/Part-time/Hourly/Contract (enables employment type analysis)

A sample template is provided in `data/sample_data.csv`

## Methodology

**Cohort Analysis**: Groups employees by hire period and tracks retention rates over time. Shows what percentage remain after 3, 6, 12, 24 months.

**Case-Based Analysis**: Categorizes terminations into 6 tenure windows:
- **Case 0**: Never Worked (0 days) - onboarding failures
- **Case 1**: Quick Exits (< 3 months) - poor fit or expectations mismatch
- **Case 2**: Post-Onboarding Crash (3-12 months) - role clarity or training issues
- **Case 3**: Mid-Term Fallout (1-3 years) - career progression or burnout
- **Case 4**: Established Turnover (3-5 years) - competitive opportunities
- **Case 5**: Veteran Turnover (5+ years) - retirement or major life changes

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
│   ├── case_analysis.py    # Case-based tenure analysis
│   ├── cost_calculator.py  # Financial impact modeling
│   ├── visualizations.py   # Chart generation (including Sankey diagrams)
│   └── predictive.py       # Risk flagging logic
└── data/
    └── sample_data.csv     # Template file (100 sample employees)
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
