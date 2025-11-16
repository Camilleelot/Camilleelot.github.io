"""
Predictive analysis module
Identifies at-risk employees and patterns
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def identify_high_risk_tenure_periods(df: pd.DataFrame) -> dict:
    """
    Identify tenure periods with highest turnover risk

    Args:
        df: Employee dataframe

    Returns:
        Dictionary with risk periods
    """
    terminated = df[~df['is_active']].copy()

    if len(terminated) == 0:
        return {'risk_periods': [], 'insights': []}

    # Analyze when people are most likely to leave
    tenure_buckets = pd.cut(
        terminated['tenure_days'],
        bins=[0, 90, 180, 365, 730, 1095, float('inf')],
        labels=['0-3mo', '3-6mo', '6-12mo', '1-2yr', '2-3yr', '3yr+']
    )

    risk_dist = tenure_buckets.value_counts(normalize=True).sort_values(ascending=False)

    insights = []
    if len(risk_dist) > 0:
        highest_risk = risk_dist.index[0]
        risk_pct = risk_dist.values[0] * 100
        insights.append(f"{highest_risk} is the highest risk period ({risk_pct:.0f}% of terminations)")

    return {
        'risk_periods': risk_dist.to_dict(),
        'insights': insights,
        'highest_risk_period': risk_dist.index[0] if len(risk_dist) > 0 else None
    }


def flag_at_risk_employees(df: pd.DataFrame, risk_criteria: dict = None) -> pd.DataFrame:
    """
    Flag currently active employees who may be at risk of leaving

    Args:
        df: Employee dataframe
        risk_criteria: Custom risk thresholds

    Returns:
        DataFrame of at-risk active employees
    """
    if risk_criteria is None:
        risk_criteria = {
            'high_risk_tenure_min': 60,   # Days
            'high_risk_tenure_max': 180,  # Days
            'dept_high_turnover_threshold': 30  # Percent
        }

    active = df[df['is_active']].copy()

    if len(active) == 0:
        return pd.DataFrame()

    # Calculate department turnover rates
    dept_turnover = df.groupby('department').apply(
        lambda x: (~x['is_active']).sum() / len(x) * 100 if len(x) > 0 else 0
    ).to_dict()

    active['dept_turnover_rate'] = active['department'].map(dept_turnover)

    # Flag risk factors
    active['risk_score'] = 0
    active['risk_factors'] = ''

    # Risk Factor 1: In high-risk tenure window
    in_risk_window = (
        (active['tenure_days'] >= risk_criteria['high_risk_tenure_min']) &
        (active['tenure_days'] <= risk_criteria['high_risk_tenure_max'])
    )
    active.loc[in_risk_window, 'risk_score'] += 2
    active.loc[in_risk_window, 'risk_factors'] += 'High-risk tenure period; '

    # Risk Factor 2: In high-turnover department
    high_turnover_dept = active['dept_turnover_rate'] > risk_criteria['dept_high_turnover_threshold']
    active.loc[high_turnover_dept, 'risk_score'] += 1
    active.loc[high_turnover_dept, 'risk_factors'] += 'High-turnover department; '

    # Risk Factor 3: Recently hit 6-month or 1-year mark (common decision points)
    days_since_6mo = abs(active['tenure_days'] - 180)
    days_since_1yr = abs(active['tenure_days'] - 365)

    near_milestone = (days_since_6mo < 30) | (days_since_1yr < 30)
    active.loc[near_milestone, 'risk_score'] += 1
    active.loc[near_milestone, 'risk_factors'] += 'Near tenure milestone; '

    # Filter to employees with at least some risk
    at_risk = active[active['risk_score'] > 0].copy()

    # Add risk level
    at_risk['risk_level'] = pd.cut(
        at_risk['risk_score'],
        bins=[0, 1, 2, 10],
        labels=['Low', 'Medium', 'High']
    )

    # Clean up risk factors string
    at_risk['risk_factors'] = at_risk['risk_factors'].str.rstrip('; ')

    return at_risk[[
        'employee_id', 'name', 'department', 'tenure_days',
        'risk_score', 'risk_level', 'risk_factors', 'dept_turnover_rate'
    ]].sort_values('risk_score', ascending=False)


def predict_future_turnover(df: pd.DataFrame, forecast_months: int = 12) -> dict:
    """
    Forecast turnover for the next N months based on historical patterns

    Args:
        df: Employee dataframe
        forecast_months: Number of months to forecast

    Returns:
        Dictionary with forecast data
    """
    # Calculate historical monthly turnover rate
    terminated = df[df['termination_date'].notna()].copy()

    if len(terminated) == 0:
        return {'forecast': [], 'avg_monthly_rate': 0}

    # Get date range
    min_date = df['hire_date'].min()
    max_date = datetime.now()
    months_of_data = ((max_date.year - min_date.year) * 12 +
                      (max_date.month - min_date.month))

    if months_of_data == 0:
        return {'forecast': [], 'avg_monthly_rate': 0}

    # Calculate average monthly terminations
    total_terminations = len(terminated)
    avg_monthly_terminations = total_terminations / months_of_data

    # Calculate average headcount
    current_headcount = df['is_active'].sum()

    # Forecast
    forecast = []
    for month in range(1, forecast_months + 1):
        forecast_date = datetime.now() + timedelta(days=30 * month)
        expected_terminations = avg_monthly_terminations

        forecast.append({
            'month': month,
            'date': forecast_date.strftime('%Y-%m'),
            'expected_terminations': expected_terminations,
            'confidence': 'Medium' if months_of_data > 12 else 'Low'
        })

    avg_monthly_rate = (avg_monthly_terminations / current_headcount * 100) if current_headcount > 0 else 0

    return {
        'forecast': forecast,
        'avg_monthly_terminations': avg_monthly_terminations,
        'avg_monthly_rate': avg_monthly_rate,
        'current_headcount': current_headcount,
        'months_of_historical_data': months_of_data
    }


def analyze_seasonal_patterns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identify seasonal turnover patterns

    Args:
        df: Employee dataframe

    Returns:
        DataFrame with turnover by month of year
    """
    terminated = df[df['termination_date'].notna()].copy()

    if len(terminated) == 0:
        return pd.DataFrame()

    # Extract month from termination date
    terminated['month'] = terminated['termination_date'].dt.month
    terminated['month_name'] = terminated['termination_date'].dt.strftime('%B')

    # Count terminations by month
    monthly = terminated.groupby(['month', 'month_name']).size().reset_index(name='terminations')
    monthly = monthly.sort_values('month')

    # Calculate as percentage of total
    monthly['percentage'] = (monthly['terminations'] / monthly['terminations'].sum() * 100)

    return monthly[['month_name', 'terminations', 'percentage']]


def calculate_turnover_velocity(df: pd.DataFrame) -> dict:
    """
    Calculate how quickly turnover is changing (acceleration/deceleration)

    Args:
        df: Employee dataframe

    Returns:
        Dictionary with velocity metrics
    """
    terminated = df[df['termination_date'].notna()].copy()

    if len(terminated) < 2:
        return {'trend': 'Insufficient data', 'velocity': 0}

    # Get terminations by quarter
    terminated['quarter'] = terminated['termination_date'].dt.to_period('Q')
    quarterly = terminated.groupby('quarter').size().reset_index(name='terminations')
    quarterly = quarterly.sort_values('quarter')

    if len(quarterly) < 2:
        return {'trend': 'Insufficient data', 'velocity': 0}

    # Calculate simple trend
    recent_avg = quarterly.tail(2)['terminations'].mean()
    older_avg = quarterly.head(2)['terminations'].mean()

    velocity = ((recent_avg - older_avg) / older_avg * 100) if older_avg > 0 else 0

    if velocity > 10:
        trend = 'Accelerating'
    elif velocity < -10:
        trend = 'Decelerating'
    else:
        trend = 'Stable'

    return {
        'trend': trend,
        'velocity': velocity,
        'recent_quarterly_avg': recent_avg,
        'older_quarterly_avg': older_avg
    }
