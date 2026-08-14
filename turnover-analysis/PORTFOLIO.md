# Portfolio Showcase: NGO Turnover Analysis Tool

## Project Overview

A production-ready data analytics tool that helps nonprofit organizations understand and reduce employee turnover through interactive visualizations and predictive insights.

**Live Demo**: [hrturnoveranalysis.streamlit.app](https://hrturnoveranalysis.streamlit.app/)
**GitHub**: [github.com/Camilleelot/Camilleelot.github.io/tree/main/turnover-analysis](https://github.com/Camilleelot/Camilleelot.github.io/tree/main/turnover-analysis)
**Tech Stack**: Python, Streamlit, Pandas, Plotly

## The Problem

Nonprofit organizations face turnover rates 20-25% higher than the private sector, costing them millions in recruitment, training, and lost productivity. Yet most NGOs lack the tools or expertise to analyze their HR data effectively.

During my time working with a large Calgary NGO, I saw firsthand how:
- HR managers worked with disconnected Excel spreadsheets
- Turnover patterns were invisible until exit interviews
- Board reports lacked quantitative backing
- Cost calculations were rough estimates at best

## The Solution

I built a self-service analytics platform that:
- Transforms raw Excel data into actionable insights
- Provides cohort analysis to identify retention patterns
- Calculates true turnover costs (not just salary replacement)
- Flags at-risk employees before they resign
- Forecasts future turnover and budget impact

## Technical Implementation

### Architecture
```
┌─────────────────┐
│  Streamlit UI   │  ← User-friendly interface
└────────┬────────┘
         │
    ┌────┴────────────────────────┐
    │                             │
┌───▼──────┐              ┌──────▼────┐
│  Data    │              │ Analytics │
│  Layer   │              │  Engine   │
└──────────┘              └───────────┘
│ - Excel loader          │ - Cohort analysis
│ - Validation            │ - Cost modeling
│ - Cleaning              │ - Predictions
│ - Transformation        │ - Visualizations
```

### Key Features Implemented

**1. Data Pipeline**
- Robust Excel ingestion with validation
- Automatic data cleaning and type inference
- Derived metrics (tenure, cohorts, risk scores)
- Error handling for malformed data

**2. Analytics Modules**
- **Cohort Analysis**: Retention heatmaps by hire cohort
- **Survival Analysis**: Kaplan-Meier style retention curves
- **Cost Modeling**: SHRM-based cost multipliers (recruitment, training, productivity loss)
- **Risk Flagging**: Transparent, rule-based risk scoring with named reasons for each flag
- **Time Series**: Turnover trends with velocity calculations

**3. Interactive Visualizations**
- Plotly charts (heatmaps, line charts, bar charts, pie charts)
- Drill-down by department, role, cohort
- Export-ready for board presentations
- Mobile-responsive layout

**4. User Experience**
- Zero-code interface for non-technical users
- Drag-and-drop file upload
- Sample data for testing
- Downloadable reports (CSV, charts)
- Adjustable cost assumptions

### Code Quality

- **Modular design**: Separate modules for data, analysis, viz, risk flagging
- **Documentation**: Docstrings for all functions, type hints
- **Error handling**: Graceful failures with user-friendly messages
- **Performance**: Efficient pandas operations, no unnecessary recomputation

## Technical Challenges Solved

### Challenge 1: Cohort Retention Calculation
Traditional cohort analysis requires complex date arithmetic. I built a system that:
- Handles active and terminated employees simultaneously
- Accounts for varying cohort sizes
- Normalizes retention rates for meaningful comparison

```python
# Key innovation: vectorized tenure calculation
df['tenure_months'] = df.apply(
    lambda row: (
        (datetime.now() if pd.isna(row['termination_date'])
         else row['termination_date']) - row['hire_date']
    ).days // 30,
    axis=1
)
```

### Challenge 2: Cost Estimation Without Salary Data
Many NGOs don't track salary in exportable formats. I implemented:
- Median imputation when salary is missing
- Adjustable multipliers for different org contexts
- Sensitivity analysis showing impact of assumptions

### Challenge 3: Risk Flagging with Limited Features
Without performance reviews or engagement scores, I built a transparent rule-based scoring system:
- Tenure-based risk windows (highest risk at 2–6 months)
- Department-level historical turnover rates
- Temporal proximity to milestone dates (6mo, 1yr anniversaries)

Each flagged employee carries a named reason (+2 for high-risk tenure window, +1 for high-turnover department, +1 for milestone proximity). Transparent and auditable > complex but opaque.

## What I Learned Building This

- First full-stack data product (not just analysis notebooks)
- Learned Streamlit for rapid prototyping
- Practiced product thinking: what do users actually need?
- Designed for a non-technical audience from the start

## Skills Demonstrated

### Data Engineering
- ETL pipeline design
- Data validation and cleaning
- Schema design and transformation
- Error handling and logging

### Data Analysis
- Cohort analysis
- Survival analysis
- Time series analysis
- Statistical modeling

### Software Engineering
- Modular code architecture
- Version control (Git)
- Documentation
- Deployment

### Product Thinking
- User research (worked with HR managers)
- Feature prioritization
- UX design for non-technical users
- Iterative development based on feedback

### Communication
- Technical documentation
- User guides
- Data visualization
- Translating complex analytics into business value

## Future Enhancements

**Version 2.0 Roadmap:**
- [ ] Integration with HRIS APIs (BambooHR, Rippling, Gusto)
- [ ] Machine learning models for turnover prediction
- [ ] Sentiment analysis on exit interview notes
- [ ] Automated email alerts for at-risk employees
- [ ] Diversity/equity metrics
- [ ] Multi-org benchmarking platform

## Lessons Learned

1. **Start with the problem, not the tech**: Initially wanted to build an ML model, but users just needed clear reporting first
2. **Simplicity wins**: Cohort heatmap was more valuable than complex survival models
3. **Data quality matters**: 50% of dev time went to handling messy real-world data
4. **Documentation is product**: Guides reduced support questions significantly

## Skills Demonstrated

This project demonstrates skills directly applicable to data analyst/engineer roles:

- **Data pipelines**: Built ETL for unstructured Excel → analyzed dataframes
- **Analytics**: Cohort analysis, cost modeling, rule-based risk scoring
- **Visualization**: Interactive dashboards with business context
- **Stakeholder communication**: Translated HR jargon into metrics
- **Python proficiency**: Pandas, NumPy, Plotly, Streamlit

It also shows:
- Identify real problems
- Build solutions independently end-to-end
- Communicate technical concepts to non-technical users

## Repository Structure

```
turnover-analysis/
├── app.py                    # Main Streamlit application
├── src/
│   ├── data_loader.py        # Excel ingestion & validation
│   ├── cohort_analysis.py    # Retention calculations
│   ├── cost_calculator.py    # Financial modeling
│   ├── visualizations.py     # Plotly chart generation
│   └── predictive.py         # Risk assessment logic
├── data/
│   └── sample_data.csv       # Demo dataset
├── README.md                 # Technical overview
├── QUICKSTART.md             # User guide
├── DEPLOYMENT.md             # DevOps instructions
└── requirements.txt          # Dependencies
```

## Try It Yourself

```bash
git clone [repo-url]
cd turnover-analysis
pip install -r requirements.txt
streamlit run app.py
```

Upload your own HR data or use the sample dataset to explore features.

---

