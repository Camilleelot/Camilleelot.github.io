# Quick Start Guide

## Installation

1. **Clone or download this repository**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Open in browser**
The app will automatically open at `http://localhost:8501`

## First Time Use

### Option 1: Use Sample Data
1. Check the "Use sample data" box in the sidebar
2. Explore all the features with demo data

### Option 2: Upload Your Own Data
1. Prepare your Excel file with these columns:
   - `employee_id` (required)
   - `name` (required)
   - `hire_date` (required, format: YYYY-MM-DD)
   - `termination_date` (optional, blank if still employed)
   - `department` (optional but recommended)
   - `role` (optional)
   - `salary` (optional but needed for cost calculations)
   - `termination_reason` (optional)

2. Click "Browse files" in the sidebar
3. Upload your `.xlsx` or `.xls` file
4. The app will validate and load your data

## Features Tour

### 📈 Overview Tab
- See high-level metrics (total employees, turnover rate)
- View turnover trends over time
- Compare departments
- Understand when employees typically leave

### 👥 Cohort Analysis Tab
- Track retention by hire cohort
- See survival curves
- Identify seasonal patterns

### 💰 Cost Analysis Tab
- Estimate total turnover costs
- Break down costs by component
- Forecast future costs
- Calculate ROI of retention initiatives

### ⚠️ Risk Assessment Tab
- Identify employees at risk of leaving
- See high-risk tenure periods
- Get turnover forecasts

### 📊 Raw Data Tab
- View and download your full dataset
- Check data quality

## Tips for Best Results

1. **More data = better insights**: At least 1-2 years of data recommended
2. **Keep salary data accurate**: Cost calculations depend on this
3. **Track termination reasons**: Helps identify voluntary vs. involuntary patterns
4. **Regular updates**: Upload fresh data monthly or quarterly

## Exporting Reports

- Most charts can be downloaded as PNG (hover → camera icon)
- Download filtered data as CSV from each tab
- For board reports: Screenshot key metrics and charts

## Troubleshooting

**Error: "Missing required columns"**
- Check your Excel column names match exactly (case-sensitive)
- Required: employee_id, name, hire_date

**Error: "Found duplicate employee IDs"**
- Each employee needs a unique ID
- Check for copy-paste errors in your data

**Charts look weird**
- Might need more data (< 5 employees)
- Check date formats are correct

**Cost calculations seem high/low**
- Adjust cost multipliers in sidebar → Advanced settings
- Default assumes 80% of salary per turnover (industry standard)

## Privacy & Security

- All processing happens locally on your computer
- No data is sent to external servers
- Your files stay on your machine
- Safe to use with confidential HR data

## Next Steps

Want to deploy this for your team? See `DEPLOYMENT.md` for instructions on:
- Deploying to Streamlit Cloud (free, shareable)
- Running on internal servers
- Setting up automated data updates
