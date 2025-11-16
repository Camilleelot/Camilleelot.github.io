"""
Turnover cost calculator module
Estimates financial impact of employee turnover
"""

import pandas as pd
import numpy as np


# Industry benchmark multipliers (based on SHRM and other HR research)
COST_MULTIPLIERS = {
    'recruitment': 0.20,      # ~20% of annual salary
    'training': 0.10,          # ~10% of annual salary
    'productivity_loss': 0.50, # ~50% of annual salary (assumes 6-month ramp)
    'total': 0.80              # ~80% of annual salary
}


def calculate_turnover_costs(
    df: pd.DataFrame,
    custom_multipliers: dict = None
) -> pd.DataFrame:
    """
    Calculate estimated turnover costs for each terminated employee

    Args:
        df: Employee dataframe with termination_date and salary
        custom_multipliers: Optional dict to override default cost multipliers

    Returns:
        DataFrame with cost estimates per employee
    """
    multipliers = COST_MULTIPLIERS.copy()
    if custom_multipliers:
        multipliers.update(custom_multipliers)

    # Filter to terminated employees only
    terminated = df[df['termination_date'].notna()].copy()

    if 'salary' not in terminated.columns:
        # Use median salary as fallback
        terminated['salary'] = 50000  # Default assumption

    # Calculate component costs
    terminated['recruitment_cost'] = terminated['salary'] * multipliers['recruitment']
    terminated['training_cost'] = terminated['salary'] * multipliers['training']
    terminated['productivity_loss'] = terminated['salary'] * multipliers['productivity_loss']
    terminated['total_turnover_cost'] = terminated['salary'] * multipliers['total']

    # Add year for grouping
    terminated['termination_year'] = terminated['termination_date'].dt.year

    return terminated[[
        'employee_id', 'name', 'termination_date', 'termination_year',
        'salary', 'recruitment_cost', 'training_cost', 'productivity_loss',
        'total_turnover_cost'
    ]]


def calculate_aggregate_costs(cost_df: pd.DataFrame) -> dict:
    """
    Calculate aggregate turnover costs across the organization

    Args:
        cost_df: Output from calculate_turnover_costs()

    Returns:
        Dictionary of aggregate cost metrics
    """
    total_costs = {
        'total_recruitment_cost': cost_df['recruitment_cost'].sum(),
        'total_training_cost': cost_df['training_cost'].sum(),
        'total_productivity_loss': cost_df['productivity_loss'].sum(),
        'total_turnover_cost': cost_df['total_turnover_cost'].sum(),
        'num_terminations': len(cost_df),
        'avg_cost_per_termination': cost_df['total_turnover_cost'].mean(),
    }

    return total_costs


def calculate_costs_by_department(
    df: pd.DataFrame,
    custom_multipliers: dict = None
) -> pd.DataFrame:
    """
    Calculate turnover costs grouped by department

    Args:
        df: Employee dataframe
        custom_multipliers: Optional custom cost multipliers

    Returns:
        DataFrame with costs by department
    """
    if 'department' not in df.columns:
        return pd.DataFrame()

    cost_df = calculate_turnover_costs(df, custom_multipliers)

    # Merge department info
    cost_df = cost_df.merge(
        df[['employee_id', 'department']],
        on='employee_id',
        how='left'
    )

    dept_costs = cost_df.groupby('department').agg({
        'total_turnover_cost': 'sum',
        'employee_id': 'count',
        'salary': 'mean'
    }).reset_index()

    dept_costs.columns = [
        'department',
        'total_cost',
        'num_terminations',
        'avg_salary'
    ]

    dept_costs['avg_cost_per_termination'] = (
        dept_costs['total_cost'] / dept_costs['num_terminations']
    )

    return dept_costs.sort_values('total_cost', ascending=False)


def calculate_costs_by_year(
    df: pd.DataFrame,
    custom_multipliers: dict = None
) -> pd.DataFrame:
    """
    Calculate turnover costs by year

    Args:
        df: Employee dataframe
        custom_multipliers: Optional custom cost multipliers

    Returns:
        DataFrame with annual costs
    """
    cost_df = calculate_turnover_costs(df, custom_multipliers)

    yearly_costs = cost_df.groupby('termination_year').agg({
        'total_turnover_cost': 'sum',
        'employee_id': 'count',
        'recruitment_cost': 'sum',
        'training_cost': 'sum',
        'productivity_loss': 'sum'
    }).reset_index()

    yearly_costs.columns = [
        'year',
        'total_cost',
        'num_terminations',
        'recruitment_cost',
        'training_cost',
        'productivity_loss'
    ]

    return yearly_costs.sort_values('year')


def forecast_annual_cost(
    df: pd.DataFrame,
    current_headcount: int,
    projected_turnover_rate: float,
    avg_salary: float = None,
    custom_multipliers: dict = None
) -> dict:
    """
    Forecast annual turnover costs based on projected rate

    Args:
        df: Historical employee dataframe
        current_headcount: Current number of employees
        projected_turnover_rate: Expected annual turnover % (e.g., 25.0 for 25%)
        avg_salary: Average salary (if None, will calculate from data)
        custom_multipliers: Optional custom cost multipliers

    Returns:
        Dictionary with forecasted costs
    """
    multipliers = COST_MULTIPLIERS.copy()
    if custom_multipliers:
        multipliers.update(custom_multipliers)

    # Use provided avg salary or calculate from data
    if avg_salary is None:
        if 'salary' in df.columns:
            avg_salary = df['salary'].median()
        else:
            avg_salary = 50000  # Default assumption

    # Calculate expected terminations
    expected_terminations = current_headcount * (projected_turnover_rate / 100)

    # Calculate forecasted costs
    forecast = {
        'current_headcount': current_headcount,
        'projected_turnover_rate': projected_turnover_rate,
        'expected_terminations': expected_terminations,
        'avg_salary': avg_salary,
        'forecasted_recruitment_cost': expected_terminations * avg_salary * multipliers['recruitment'],
        'forecasted_training_cost': expected_terminations * avg_salary * multipliers['training'],
        'forecasted_productivity_loss': expected_terminations * avg_salary * multipliers['productivity_loss'],
        'forecasted_total_cost': expected_terminations * avg_salary * multipliers['total'],
        'cost_per_termination': avg_salary * multipliers['total']
    }

    return forecast


def calculate_roi_of_retention(
    current_turnover_rate: float,
    improved_turnover_rate: float,
    current_headcount: int,
    avg_salary: float,
    retention_program_cost: float = 0,
    custom_multipliers: dict = None
) -> dict:
    """
    Calculate ROI of retention initiatives

    Args:
        current_turnover_rate: Current annual turnover %
        improved_turnover_rate: Projected turnover % with intervention
        current_headcount: Number of employees
        avg_salary: Average annual salary
        retention_program_cost: Cost of retention initiative
        custom_multipliers: Optional custom cost multipliers

    Returns:
        Dictionary with ROI analysis
    """
    multipliers = COST_MULTIPLIERS.copy()
    if custom_multipliers:
        multipliers.update(custom_multipliers)

    # Current state costs
    current_terminations = current_headcount * (current_turnover_rate / 100)
    current_cost = current_terminations * avg_salary * multipliers['total']

    # Improved state costs
    improved_terminations = current_headcount * (improved_turnover_rate / 100)
    improved_cost = improved_terminations * avg_salary * multipliers['total']

    # Calculate savings
    gross_savings = current_cost - improved_cost
    net_savings = gross_savings - retention_program_cost
    roi_percentage = (net_savings / retention_program_cost * 100) if retention_program_cost > 0 else 0

    return {
        'current_turnover_rate': current_turnover_rate,
        'improved_turnover_rate': improved_turnover_rate,
        'reduction_in_rate': current_turnover_rate - improved_turnover_rate,
        'current_annual_cost': current_cost,
        'improved_annual_cost': improved_cost,
        'gross_annual_savings': gross_savings,
        'retention_program_cost': retention_program_cost,
        'net_annual_savings': net_savings,
        'roi_percentage': roi_percentage,
        'payback_period_months': (retention_program_cost / (gross_savings / 12)) if gross_savings > 0 else float('inf')
    }
