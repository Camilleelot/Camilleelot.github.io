"""
Cohort analysis module
Calculates retention rates and survival curves
"""

import pandas as pd
import numpy as np
from datetime import datetime


def calculate_cohort_retention(df: pd.DataFrame, period: str = 'M') -> pd.DataFrame:
    """
    Calculate retention rates by hire cohort

    Args:
        df: Employee dataframe with hire_date and termination_date
        period: Cohort period ('M' for month, 'Q' for quarter, 'Y' for year)

    Returns:
        DataFrame with cohort retention rates over time
    """
    df = df.copy()

    # Create cohort column
    df['cohort'] = df['hire_date'].dt.to_period(period).astype(str)

    # For each employee, calculate months since hire at termination or now
    current_date = datetime.now()

    def get_tenure_months(row):
        end_date = row['termination_date'] if pd.notna(row['termination_date']) else current_date
        months = (end_date.year - row['hire_date'].year) * 12 + \
                 (end_date.month - row['hire_date'].month)
        return max(0, months)

    df['tenure_months'] = df.apply(get_tenure_months, axis=1)

    # Build retention matrix
    cohorts = df.groupby('cohort')
    retention_data = []

    for cohort_name, cohort_df in cohorts:
        cohort_size = len(cohort_df)

        # Calculate retention at each month mark
        for month in range(0, 37, 3):  # 0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36
            # How many from this cohort lasted at least this many months?
            retained = (cohort_df['tenure_months'] >= month).sum()
            retention_rate = (retained / cohort_size * 100) if cohort_size > 0 else 0

            retention_data.append({
                'cohort': cohort_name,
                'months': month,
                'retained': retained,
                'cohort_size': cohort_size,
                'retention_rate': retention_rate
            })

    return pd.DataFrame(retention_data)


def calculate_turnover_by_period(df: pd.DataFrame, period: str = 'Q') -> pd.DataFrame:
    """
    Calculate turnover rate by time period

    Args:
        df: Employee dataframe
        period: Time period ('M', 'Q', 'Y')

    Returns:
        DataFrame with turnover rates per period
    """
    df = df.copy()

    # Filter to only terminated employees
    terminated = df[df['termination_date'].notna()].copy()

    if len(terminated) == 0:
        return pd.DataFrame(columns=['period', 'terminations', 'avg_headcount', 'turnover_rate'])

    # Group by termination period
    terminated['period'] = terminated['termination_date'].dt.to_period(period).astype(str)

    # Count terminations per period
    term_counts = terminated.groupby('period').size().reset_index(name='terminations')

    # Estimate average headcount per period (simplified)
    # In reality, you'd want daily headcount snapshots
    all_periods = pd.period_range(
        start=df['hire_date'].min(),
        end=datetime.now(),
        freq=period
    ).astype(str)

    results = []
    for p in all_periods:
        period_end = pd.Period(p, freq=period).end_time

        # Count active employees at end of period
        active = df[
            (df['hire_date'] <= period_end) &
            ((df['termination_date'].isna()) | (df['termination_date'] > period_end))
        ]
        headcount = len(active)

        # Get terminations in this period
        terms = term_counts[term_counts['period'] == p]['terminations'].values
        term_count = terms[0] if len(terms) > 0 else 0

        # Calculate turnover rate (annualized for non-yearly periods)
        if headcount > 0:
            if period == 'M':
                turnover_rate = (term_count / headcount) * 12 * 100
            elif period == 'Q':
                turnover_rate = (term_count / headcount) * 4 * 100
            else:  # Y
                turnover_rate = (term_count / headcount) * 100
        else:
            turnover_rate = 0

        results.append({
            'period': p,
            'terminations': term_count,
            'avg_headcount': headcount,
            'turnover_rate': turnover_rate
        })

    return pd.DataFrame(results)


def calculate_department_turnover(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate turnover rates by department

    Args:
        df: Employee dataframe

    Returns:
        DataFrame with department-level turnover stats
    """
    if 'department' not in df.columns:
        return pd.DataFrame()

    dept_stats = []

    for dept in df['department'].dropna().unique():
        dept_df = df[df['department'] == dept]

        total = len(dept_df)
        terminated = (~dept_df['is_active']).sum()
        active = dept_df['is_active'].sum()

        turnover_rate = (terminated / total * 100) if total > 0 else 0
        avg_tenure_days = dept_df['tenure_days'].mean()

        dept_stats.append({
            'department': dept,
            'total_employees': total,
            'active': active,
            'terminated': terminated,
            'turnover_rate': turnover_rate,
            'avg_tenure_days': avg_tenure_days
        })

    return pd.DataFrame(dept_stats).sort_values('turnover_rate', ascending=False)


def calculate_tenure_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate distribution of when employees leave (tenure buckets)

    Args:
        df: Employee dataframe

    Returns:
        DataFrame with tenure bucket analysis
    """
    terminated = df[~df['is_active']].copy()

    if len(terminated) == 0:
        return pd.DataFrame()

    # Create tenure buckets
    bins = [0, 90, 180, 365, 730, 1095, 1825, float('inf')]
    labels = ['0-3 mo', '3-6 mo', '6-12 mo', '1-2 yr', '2-3 yr', '3-5 yr', '5+ yr']

    terminated['tenure_bucket'] = pd.cut(
        terminated['tenure_days'],
        bins=bins,
        labels=labels,
        right=False
    )

    bucket_counts = terminated['tenure_bucket'].value_counts().reset_index()
    bucket_counts.columns = ['tenure_bucket', 'count']
    bucket_counts['percentage'] = (bucket_counts['count'] / len(terminated) * 100)

    # Ensure all buckets are present
    all_buckets = pd.DataFrame({'tenure_bucket': labels})
    result = all_buckets.merge(bucket_counts, on='tenure_bucket', how='left').fillna(0)

    return result.sort_values('tenure_bucket')


def calculate_survival_curve(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate Kaplan-Meier style survival curve

    Args:
        df: Employee dataframe

    Returns:
        DataFrame with survival probabilities by month
    """
    df = df.copy()

    max_months = 60  # Track up to 5 years
    survival_data = []

    for month in range(0, max_months + 1):
        # At-risk: employees hired at least this many months ago
        at_risk = df[df['tenure_months'] >= month]

        # Still employed: those who lasted at least this long
        survived = len(at_risk)
        total_at_risk = len(df[
            (datetime.now() - df['hire_date']).dt.days >= (month * 30)
        ])

        survival_rate = (survived / total_at_risk * 100) if total_at_risk > 0 else 0

        survival_data.append({
            'month': month,
            'survived': survived,
            'total_at_risk': total_at_risk,
            'survival_rate': survival_rate
        })

    return pd.DataFrame(survival_data)
