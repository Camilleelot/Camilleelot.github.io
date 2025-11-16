"""
Data loading and validation module
Handles Excel uploads and ensures data quality
"""

import pandas as pd
from datetime import datetime
from typing import Tuple, List


def load_excel(file) -> pd.DataFrame:
    """
    Load employee data from Excel file

    Args:
        file: Uploaded file object from Streamlit

    Returns:
        DataFrame with validated employee data
    """
    df = pd.read_excel(file)
    return df


def validate_data(df: pd.DataFrame) -> Tuple[bool, List[str]]:
    """
    Validate that required columns exist and data is clean

    Args:
        df: Input dataframe

    Returns:
        (is_valid, list_of_errors)
    """
    errors = []
    required_columns = ['employee_id', 'name', 'hire_date']

    # Check required columns
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        errors.append(f"Missing required columns: {', '.join(missing_cols)}")

    # Check for empty dataframe
    if len(df) == 0:
        errors.append("File contains no data rows")

    # Check for duplicate employee IDs
    if 'employee_id' in df.columns:
        duplicates = df['employee_id'].duplicated().sum()
        if duplicates > 0:
            errors.append(f"Found {duplicates} duplicate employee IDs")

    return (len(errors) == 0, errors)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and prepare data for analysis

    Args:
        df: Raw dataframe

    Returns:
        Cleaned dataframe
    """
    df = df.copy()

    # Convert date columns
    date_columns = ['hire_date', 'termination_date']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Add calculated fields
    df['is_active'] = df['termination_date'].isna()

    # Calculate tenure in days
    df['tenure_days'] = df.apply(
        lambda row: (
            (datetime.now() if pd.isna(row['termination_date'])
             else row['termination_date']) - row['hire_date']
        ).days if pd.notna(row['hire_date']) else None,
        axis=1
    )

    # Calculate tenure in months (for survival analysis)
    df['tenure_months'] = df['tenure_days'] / 30.0

    # Extract hire cohort (year-month)
    df['hire_cohort'] = df['hire_date'].dt.to_period('M').astype(str)

    # Extract hire year
    df['hire_year'] = df['hire_date'].dt.year

    # Clean text fields
    text_columns = ['department', 'role', 'termination_reason']
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace('nan', None)

    return df


def get_data_summary(df: pd.DataFrame) -> dict:
    """
    Generate summary statistics about the dataset

    Args:
        df: Cleaned dataframe

    Returns:
        Dictionary of summary stats
    """
    summary = {
        'total_employees': len(df),
        'active_employees': df['is_active'].sum(),
        'terminated_employees': (~df['is_active']).sum(),
        'date_range_start': df['hire_date'].min(),
        'date_range_end': df['hire_date'].max(),
        'departments': df['department'].nunique() if 'department' in df.columns else 0,
        'avg_tenure_days': df['tenure_days'].mean(),
    }

    # Calculate overall turnover rate
    if summary['total_employees'] > 0:
        summary['turnover_rate'] = (
            summary['terminated_employees'] / summary['total_employees'] * 100
        )
    else:
        summary['turnover_rate'] = 0

    return summary


def create_sample_template() -> pd.DataFrame:
    """
    Create a sample dataset for demonstration

    Returns:
        Sample dataframe
    """
    sample_data = {
        'employee_id': [1001, 1002, 1003, 1004, 1005, 1006, 1007, 1008],
        'name': ['Alice Johnson', 'Bob Smith', 'Carol Williams', 'David Brown',
                 'Emma Davis', 'Frank Miller', 'Grace Wilson', 'Henry Moore'],
        'hire_date': ['2022-01-15', '2022-03-01', '2022-06-10', '2022-08-20',
                      '2023-01-05', '2023-04-12', '2023-07-01', '2023-10-15'],
        'termination_date': [None, '2023-02-15', None, '2022-12-01',
                             None, None, '2024-08-30', None],
        'department': ['Programs', 'Programs', 'Development', 'Operations',
                       'Programs', 'Development', 'Operations', 'Programs'],
        'role': ['Coordinator', 'Manager', 'Officer', 'Specialist',
                 'Associate', 'Manager', 'Coordinator', 'Associate'],
        'termination_reason': [None, 'Voluntary', None, 'Voluntary',
                               None, None, 'Involuntary', None],
        'salary': [45000, 65000, 52000, 58000, 48000, 70000, 50000, 47000],
    }

    return pd.DataFrame(sample_data)
