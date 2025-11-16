"""
Case type analysis module
Categorizes terminations by tenure windows and patterns
Based on real-world NGO turnover research
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple


# Define case types based on tenure windows
CASE_DEFINITIONS = {
    'Case 0': {
        'name': 'Never Worked',
        'tenure_min': 0,
        'tenure_max': 0,
        'description': 'Employees who never actually started (0 days)',
        'color': '#e74c3c'
    },
    'Case 1': {
        'name': 'Quick Exits',
        'tenure_min': 1,
        'tenure_max': 90,
        'description': 'Left before 3 months (onboarding failure)',
        'color': '#e67e22'
    },
    'Case 2': {
        'name': 'Post-Onboarding Crash',
        'tenure_min': 91,
        'tenure_max': 365,
        'description': 'Left between 3-12 months (role mismatch)',
        'color': '#f39c12'
    },
    'Case 3': {
        'name': 'Mid-Term Fallout',
        'tenure_min': 366,
        'tenure_max': 1095,
        'description': 'Left between 1-3 years (career progression)',
        'color': '#f1c40f'
    },
    'Case 4': {
        'name': 'Established Turnover',
        'tenure_min': 1096,
        'tenure_max': 1825,
        'description': 'Left between 3-5 years (experienced staff)',
        'color': '#3498db'
    },
    'Case 5': {
        'name': 'Veteran Turnover',
        'tenure_min': 1826,
        'tenure_max': float('inf'),
        'description': 'Left after 5+ years (institutional knowledge loss)',
        'color': '#9b59b6'
    }
}


def assign_case_type(df: pd.DataFrame, only_terminated: bool = True) -> pd.DataFrame:
    """
    Assign case types to employees based on tenure at termination

    Args:
        df: Employee dataframe with tenure_days
        only_terminated: If True, only assign cases to terminated employees

    Returns:
        DataFrame with case_type column added
    """
    df = df.copy()

    # Filter to terminated only if requested
    if only_terminated:
        working_df = df[~df['is_active']].copy()
    else:
        working_df = df.copy()

    # Initialize case_type column
    df['case_type'] = None
    df['case_name'] = None

    # Assign case types based on tenure
    for case_id, case_info in CASE_DEFINITIONS.items():
        mask = (
            (working_df['tenure_days'] >= case_info['tenure_min']) &
            (working_df['tenure_days'] <= case_info['tenure_max'])
        )

        df.loc[working_df[mask].index, 'case_type'] = case_id
        df.loc[working_df[mask].index, 'case_name'] = case_info['name']

    return df


def calculate_case_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate distribution of terminations across case types

    Args:
        df: Employee dataframe with case_type assigned

    Returns:
        DataFrame with case distribution metrics
    """
    terminated = df[~df['is_active']].copy()

    if 'case_type' not in terminated.columns:
        terminated = assign_case_type(terminated)

    # Count by case type
    case_counts = terminated.groupby(['case_type', 'case_name']).size().reset_index(name='count')

    # Add percentages
    total_terminated = len(terminated)
    case_counts['percentage'] = (case_counts['count'] / total_terminated * 100)

    # Add case definitions
    case_counts['description'] = case_counts['case_type'].map(
        lambda x: CASE_DEFINITIONS[x]['description'] if x in CASE_DEFINITIONS else ''
    )

    # Sort by case order
    case_order = list(CASE_DEFINITIONS.keys())
    case_counts['sort_order'] = case_counts['case_type'].map(
        lambda x: case_order.index(x) if x in case_order else 999
    )
    case_counts = case_counts.sort_values('sort_order').drop('sort_order', axis=1)

    return case_counts


def calculate_case_by_role(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Calculate case distribution by role

    Args:
        df: Employee dataframe
        top_n: Number of top roles to include

    Returns:
        DataFrame with role x case breakdown
    """
    if 'role' not in df.columns:
        return pd.DataFrame()

    terminated = df[~df['is_active']].copy()

    if 'case_type' not in terminated.columns:
        terminated = assign_case_type(terminated)

    # Get top N roles by termination count
    top_roles = terminated['role'].value_counts().head(top_n).index

    # Filter to top roles
    role_cases = terminated[terminated['role'].isin(top_roles)].copy()

    # Create pivot table
    pivot = pd.crosstab(
        role_cases['role'],
        role_cases['case_type'],
        normalize='index'
    ) * 100

    # Add total count column
    pivot['total_terminations'] = terminated['role'].value_counts()

    # Reorder columns by case order
    case_order = [c for c in CASE_DEFINITIONS.keys() if c in pivot.columns]
    pivot = pivot[case_order + ['total_terminations']]

    # Sort by total terminations
    pivot = pivot.sort_values('total_terminations', ascending=False)

    return pivot


def calculate_voluntary_by_case(df: pd.DataFrame) -> pd.DataFrame:
    """
    Break down voluntary vs involuntary terminations by case type

    Args:
        df: Employee dataframe with termination_reason

    Returns:
        DataFrame with voluntary/involuntary split by case
    """
    if 'termination_reason' not in df.columns:
        return pd.DataFrame()

    terminated = df[~df['is_active']].copy()

    if 'case_type' not in terminated.columns:
        terminated = assign_case_type(terminated)

    # Create voluntary flag
    terminated['is_voluntary'] = terminated['termination_reason'].str.lower().str.contains(
        'voluntary', na=False
    )

    # Group by case and voluntary status
    case_voluntary = terminated.groupby(['case_type', 'case_name', 'is_voluntary']).size().unstack(fill_value=0)

    # Calculate percentages
    case_voluntary['total'] = case_voluntary.sum(axis=1)
    if False in case_voluntary.columns:
        case_voluntary['involuntary_pct'] = (case_voluntary[False] / case_voluntary['total'] * 100)
    else:
        case_voluntary['involuntary_pct'] = 0

    if True in case_voluntary.columns:
        case_voluntary['voluntary_pct'] = (case_voluntary[True] / case_voluntary['total'] * 100)
    else:
        case_voluntary['voluntary_pct'] = 0

    # Rename columns for clarity
    result = case_voluntary.reset_index()
    if False in result.columns:
        result = result.rename(columns={False: 'involuntary_count'})
    else:
        result['involuntary_count'] = 0

    if True in result.columns:
        result = result.rename(columns={True: 'voluntary_count'})
    else:
        result['voluntary_count'] = 0

    return result


def identify_high_risk_roles(df: pd.DataFrame, case_window: str = 'Case 2') -> pd.DataFrame:
    """
    Identify roles with highest turnover in a specific case window

    Args:
        df: Employee dataframe
        case_window: Which case to analyze (e.g., 'Case 2')

    Returns:
        DataFrame with role breakdown for that case
    """
    terminated = df[~df['is_active']].copy()

    if 'case_type' not in terminated.columns:
        terminated = assign_case_type(terminated)

    # Filter to specific case
    case_data = terminated[terminated['case_type'] == case_window].copy()

    if len(case_data) == 0:
        return pd.DataFrame()

    # Count by role
    role_counts = case_data['role'].value_counts().reset_index()
    role_counts.columns = ['role', 'count']

    # Calculate percentage of this case's total
    role_counts['pct_of_case'] = (role_counts['count'] / len(case_data) * 100)

    # Calculate percentage of all voluntary exits (if applicable)
    all_terminated = len(terminated)
    role_counts['pct_of_all_terminations'] = (role_counts['count'] / all_terminated * 100)

    return role_counts.sort_values('count', ascending=False)


def calculate_year_over_year_cases(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate case distribution changes year over year

    Args:
        df: Employee dataframe with termination_date

    Returns:
        DataFrame with YoY case trends
    """
    terminated = df[~df['is_active']].copy()

    if 'case_type' not in terminated.columns:
        terminated = assign_case_type(terminated)

    # Extract fiscal year (assuming April 1 start)
    terminated['fiscal_year'] = terminated['termination_date'].apply(
        lambda x: x.year if x.month >= 4 else x.year - 1
    )

    # Group by fiscal year and case
    yoy = terminated.groupby(['fiscal_year', 'case_type']).size().reset_index(name='count')

    # Pivot
    pivot = yoy.pivot(index='case_type', columns='fiscal_year', values='count').fillna(0)

    # Calculate percentages
    for col in pivot.columns:
        total = pivot[col].sum()
        pivot[f'{col}_pct'] = (pivot[col] / total * 100) if total > 0 else 0

    return pivot


def generate_case_insights(df: pd.DataFrame) -> List[str]:
    """
    Generate automated insights about case patterns

    Args:
        df: Employee dataframe

    Returns:
        List of insight strings
    """
    insights = []

    terminated = df[~df['is_active']].copy()

    if 'case_type' not in terminated.columns:
        terminated = assign_case_type(terminated)

    # Overall case distribution
    case_dist = calculate_case_distribution(df)

    # Biggest case
    biggest_case = case_dist.loc[case_dist['percentage'].idxmax()]
    insights.append(
        f"**Largest vulnerability window**: {biggest_case['case_name']} ({biggest_case['case_type']}) "
        f"accounts for {biggest_case['percentage']:.1f}% of all terminations"
    )

    # First year attrition
    first_year_cases = case_dist[case_dist['case_type'].isin(['Case 1', 'Case 2'])]
    first_year_pct = first_year_cases['percentage'].sum()
    insights.append(
        f"**First-year attrition**: {first_year_pct:.1f}% of turnover happens in the first 12 months"
    )

    # Veteran retention
    veteran_case = case_dist[case_dist['case_type'] == 'Case 5']
    if len(veteran_case) > 0:
        veteran_pct = veteran_case['percentage'].values[0]
        insights.append(
            f"**Veteran retention**: {veteran_pct:.1f}% of turnover is from employees with 5+ years tenure"
        )

    # Role-specific insight
    if 'role' in df.columns:
        role_case = calculate_case_by_role(df, top_n=3)
        if len(role_case) > 0:
            top_role = role_case.index[0]
            insights.append(
                f"**Highest-impact role**: {top_role} has {role_case.loc[top_role, 'total_terminations']:.0f} total terminations"
            )

    # Voluntary vs involuntary
    if 'termination_reason' in df.columns:
        vol_breakdown = calculate_voluntary_by_case(df)
        if len(vol_breakdown) > 0:
            overall_vol = terminated['termination_reason'].str.lower().str.contains('voluntary', na=False).mean() * 100
            insights.append(
                f"**Voluntary rate**: {overall_vol:.1f}% of terminations are voluntary across all cases"
            )

    return insights


def create_sankey_data(df: pd.DataFrame) -> Dict:
    """
    Prepare data for Sankey diagram: Department → Role → Outcome (Case or Active)

    Args:
        df: Employee dataframe

    Returns:
        Dictionary with source, target, value, labels for Sankey diagram
    """
    df = df.copy()

    # Ensure case types are assigned
    if 'case_type' not in df.columns:
        df = assign_case_type(df, only_terminated=False)

    # Create outcome: either case type or "Still Employed"
    df['outcome'] = df['case_type'].fillna('Still Employed')

    # Check required columns
    if 'department' not in df.columns or 'role' not in df.columns:
        return {'source': [], 'target': [], 'value': [], 'labels': []}

    # Create unique labels
    labels = []
    label_dict = {}

    def get_label_idx(label, prefix=''):
        full_label = f"{prefix}: {label}" if prefix else label
        if full_label not in label_dict:
            label_dict[full_label] = len(labels)
            labels.append(full_label)
        return label_dict[full_label]

    # Build flows
    sources = []
    targets = []
    values = []

    # Department → Role
    dept_role = df.groupby(['department', 'role']).size().reset_index(name='count')
    for _, row in dept_role.iterrows():
        dept_idx = get_label_idx(row['department'], 'Dept')
        role_idx = get_label_idx(row['role'], 'Role')
        sources.append(dept_idx)
        targets.append(role_idx)
        values.append(row['count'])

    # Role → Outcome
    role_outcome = df.groupby(['role', 'outcome']).size().reset_index(name='count')
    for _, row in role_outcome.iterrows():
        role_idx = get_label_idx(row['role'], 'Role')
        outcome_idx = get_label_idx(row['outcome'], 'Outcome')
        sources.append(role_idx)
        targets.append(outcome_idx)
        values.append(row['count'])

    return {
        'source': sources,
        'target': targets,
        'value': values,
        'labels': labels
    }


def calculate_employment_type_by_case(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyze employment type distribution across cases

    Args:
        df: Employee dataframe with employment_type

    Returns:
        DataFrame with employment type breakdown by case
    """
    if 'employment_type' not in df.columns:
        return pd.DataFrame()

    terminated = df[~df['is_active']].copy()

    if 'case_type' not in terminated.columns:
        terminated = assign_case_type(terminated)

    # Cross-tabulation
    emp_case = pd.crosstab(
        terminated['employment_type'],
        terminated['case_type'],
        normalize='columns'
    ) * 100

    # Add total counts
    emp_case['total_count'] = terminated['employment_type'].value_counts()

    return emp_case
