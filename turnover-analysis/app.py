"""
NGO Turnover Analysis Tool
Main Streamlit Application
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from data_loader import (
    load_excel, validate_data, clean_data,
    get_data_summary, create_sample_template
)
from cohort_analysis import (
    calculate_cohort_retention, calculate_turnover_by_period,
    calculate_department_turnover, calculate_tenure_distribution,
    calculate_survival_curve
)
from cost_calculator import (
    calculate_turnover_costs, calculate_aggregate_costs,
    calculate_costs_by_department, calculate_costs_by_year,
    forecast_annual_cost, calculate_roi_of_retention
)
from visualizations import (
    plot_cohort_retention, plot_turnover_trend, plot_department_comparison,
    plot_tenure_distribution, plot_cost_breakdown, plot_cost_by_department,
    plot_yearly_costs, plot_survival_curve
)
from predictive import (
    identify_high_risk_tenure_periods, flag_at_risk_employees,
    predict_future_turnover, analyze_seasonal_patterns,
    calculate_turnover_velocity
)


# Page config
st.set_page_config(
    page_title="NGO Turnover Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    st.title("📊 NGO Turnover Analysis Tool")
    st.markdown("Transform your employee data into actionable insights")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")

        # Data upload
        st.subheader("1. Upload Data")
        uploaded_file = st.file_uploader(
            "Upload your Excel file",
            type=['xlsx', 'xls'],
            help="Upload employee data with columns: employee_id, name, hire_date, termination_date, department, role, salary"
        )

        use_sample = st.checkbox("Use sample data", value=True if uploaded_file is None else False)

        # Cost multipliers (advanced)
        with st.expander("Advanced: Cost Multipliers"):
            st.markdown("Adjust cost assumptions (% of annual salary)")
            recruitment_mult = st.slider("Recruitment", 0, 50, 20) / 100
            training_mult = st.slider("Training", 0, 50, 10) / 100
            productivity_mult = st.slider("Productivity Loss", 0, 100, 50) / 100

            custom_multipliers = {
                'recruitment': recruitment_mult,
                'training': training_mult,
                'productivity_loss': productivity_mult,
                'total': recruitment_mult + training_mult + productivity_mult
            }

    # Load data
    if uploaded_file is not None:
        try:
            df = load_excel(uploaded_file)
            is_valid, errors = validate_data(df)

            if not is_valid:
                st.error("Data validation failed:")
                for error in errors:
                    st.error(f"• {error}")
                st.stop()

            df = clean_data(df)
            st.success(f"✅ Loaded {len(df)} employee records")

        except Exception as e:
            st.error(f"Error loading file: {e}")
            st.stop()

    elif use_sample:
        df = create_sample_template()
        df = clean_data(df)
        st.info("📝 Using sample data for demonstration")
    else:
        st.warning("👆 Please upload an Excel file or use sample data to get started")
        st.markdown("### Template Format")
        st.markdown("Your Excel file should include these columns:")
        st.code("""
employee_id | name | hire_date | termination_date | department | role | salary
1001 | John Doe | 2022-01-15 | | Programs | Manager | 65000
1002 | Jane Smith | 2021-06-01 | 2023-03-15 | Development | Officer | 52000
        """)

        # Download template
        template = create_sample_template()
        st.download_button(
            "📥 Download Template",
            template.to_csv(index=False),
            "turnover_analysis_template.csv",
            "text/csv"
        )
        st.stop()

    # Main dashboard
    tabs = st.tabs([
        "📈 Overview",
        "👥 Cohort Analysis",
        "💰 Cost Analysis",
        "⚠️ Risk Assessment",
        "📊 Raw Data"
    ])

    # ==================== OVERVIEW TAB ====================
    with tabs[0]:
        st.header("Overview")

        # Summary metrics
        summary = get_data_summary(df)

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Employees", f"{summary['total_employees']:,}")
        with col2:
            st.metric("Currently Active", f"{summary['active_employees']:,}")
        with col3:
            st.metric("Terminated", f"{summary['terminated_employees']:,}")
        with col4:
            st.metric("Overall Turnover Rate", f"{summary['turnover_rate']:.1f}%")

        st.markdown("---")

        # Turnover trend
        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Turnover Trend Over Time")
            turnover_trend = calculate_turnover_by_period(df, period='Q')
            if not turnover_trend.empty:
                fig = plot_turnover_trend(turnover_trend)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No turnover data available")

        with col2:
            st.subheader("Turnover Velocity")
            velocity = calculate_turnover_velocity(df)
            st.metric(
                "Trend",
                velocity['trend'],
                f"{velocity['velocity']:.1f}%",
                delta_color="inverse"
            )
            st.caption("Is turnover accelerating or slowing?")

        # Department comparison
        st.subheader("Turnover by Department")
        dept_turnover = calculate_department_turnover(df)
        if not dept_turnover.empty:
            fig = plot_department_comparison(dept_turnover)
            st.plotly_chart(fig, use_container_width=True)

            st.dataframe(
                dept_turnover,
                use_container_width=True,
                hide_index=True
            )
        else:
            st.info("Department data not available")

        # Tenure distribution
        st.subheader("When Do Employees Leave?")
        tenure_dist = calculate_tenure_distribution(df)
        if not tenure_dist.empty:
            fig = plot_tenure_distribution(tenure_dist)
            st.plotly_chart(fig, use_container_width=True)

    # ==================== COHORT ANALYSIS TAB ====================
    with tabs[1]:
        st.header("Cohort Analysis")
        st.markdown("Track retention rates by hire cohort over time")

        # Cohort retention heatmap
        st.subheader("Retention Heatmap")
        cohort_retention = calculate_cohort_retention(df, period='M')
        if not cohort_retention.empty:
            fig = plot_cohort_retention(cohort_retention)
            st.plotly_chart(fig, use_container_width=True)

            st.caption("💡 **How to read**: Each row is a hire cohort. Numbers show % still employed after N months.")
        else:
            st.info("Insufficient data for cohort analysis")

        # Survival curve
        st.subheader("Employee Retention Curve")
        survival = calculate_survival_curve(df)
        if not survival.empty:
            fig = plot_survival_curve(survival)
            st.plotly_chart(fig, use_container_width=True)

            # Key milestones
            col1, col2, col3, col4 = st.columns(4)
            milestones = [3, 6, 12, 24]
            for col, month in zip([col1, col2, col3, col4], milestones):
                if month in survival['month'].values:
                    rate = survival[survival['month'] == month]['survival_rate'].values[0]
                    with col:
                        st.metric(f"{month}-Month Retention", f"{rate:.0f}%")

        # Seasonal patterns
        st.subheader("Seasonal Patterns")
        seasonal = analyze_seasonal_patterns(df)
        if not seasonal.empty:
            st.bar_chart(seasonal.set_index('month_name')['terminations'])
            st.dataframe(seasonal, use_container_width=True, hide_index=True)
        else:
            st.info("Insufficient data for seasonal analysis")

    # ==================== COST ANALYSIS TAB ====================
    with tabs[2]:
        st.header("Cost Analysis")
        st.markdown("Estimate the financial impact of turnover")

        # Calculate costs
        cost_df = calculate_turnover_costs(df, custom_multipliers)
        cost_summary = calculate_aggregate_costs(cost_df)

        # Top-line metrics
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                "Total Turnover Cost",
                f"${cost_summary['total_turnover_cost']:,.0f}"
            )
        with col2:
            st.metric(
                "Avg Cost per Termination",
                f"${cost_summary['avg_cost_per_termination']:,.0f}"
            )
        with col3:
            st.metric(
                "Total Terminations",
                f"{cost_summary['num_terminations']:,}"
            )

        # Cost breakdown
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Cost Breakdown")
            fig = plot_cost_breakdown(cost_summary)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("Cost Components")
            st.metric("Recruitment Costs", f"${cost_summary['total_recruitment_cost']:,.0f}")
            st.metric("Training Costs", f"${cost_summary['total_training_cost']:,.0f}")
            st.metric("Productivity Loss", f"${cost_summary['total_productivity_loss']:,.0f}")

        # Department costs
        st.subheader("Costs by Department")
        dept_costs = calculate_costs_by_department(df, custom_multipliers)
        if not dept_costs.empty:
            fig = plot_cost_by_department(dept_costs)
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(dept_costs, use_container_width=True, hide_index=True)

        # Yearly costs
        st.subheader("Annual Cost Trends")
        yearly_costs = calculate_costs_by_year(df, custom_multipliers)
        if not yearly_costs.empty:
            fig = plot_yearly_costs(yearly_costs)
            st.plotly_chart(fig, use_container_width=True)

        # Future forecast
        st.subheader("Cost Forecasting")
        col1, col2 = st.columns(2)
        with col1:
            current_hc = st.number_input("Current Headcount", value=summary['active_employees'], min_value=1)
            projected_rate = st.number_input("Projected Turnover Rate (%)", value=summary['turnover_rate'], min_value=0.0, max_value=100.0)

        forecast = forecast_annual_cost(df, current_hc, projected_rate, custom_multipliers=custom_multipliers)

        with col2:
            st.metric("Expected Annual Terminations", f"{forecast['expected_terminations']:.0f}")
            st.metric("Forecasted Annual Cost", f"${forecast['forecasted_total_cost']:,.0f}")

        # ROI Calculator
        with st.expander("💡 ROI of Retention Initiatives"):
            st.markdown("Calculate potential savings from reducing turnover")

            col1, col2 = st.columns(2)
            with col1:
                improved_rate = st.number_input(
                    "Target Turnover Rate (%)",
                    value=max(0, summary['turnover_rate'] - 5),
                    min_value=0.0
                )
                program_cost = st.number_input(
                    "Retention Program Cost ($)",
                    value=10000,
                    min_value=0
                )

            avg_salary = df['salary'].median() if 'salary' in df.columns else 50000

            roi = calculate_roi_of_retention(
                summary['turnover_rate'],
                improved_rate,
                current_hc,
                avg_salary,
                program_cost,
                custom_multipliers
            )

            with col2:
                st.metric("Annual Savings", f"${roi['net_annual_savings']:,.0f}")
                st.metric("ROI", f"{roi['roi_percentage']:.0f}%")
                if roi['payback_period_months'] != float('inf'):
                    st.metric("Payback Period", f"{roi['payback_period_months']:.1f} months")

    # ==================== RISK ASSESSMENT TAB ====================
    with tabs[3]:
        st.header("Risk Assessment")
        st.markdown("Identify employees and patterns that signal turnover risk")

        # High risk periods
        st.subheader("High-Risk Tenure Periods")
        risk_periods = identify_high_risk_tenure_periods(df)
        if risk_periods['insights']:
            for insight in risk_periods['insights']:
                st.warning(insight)

        # At-risk employees
        st.subheader("⚠️ At-Risk Employees")
        at_risk = flag_at_risk_employees(df)

        if not at_risk.empty:
            # Summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("High Risk", len(at_risk[at_risk['risk_level'] == 'High']))
            with col2:
                st.metric("Medium Risk", len(at_risk[at_risk['risk_level'] == 'Medium']))
            with col3:
                st.metric("Low Risk", len(at_risk[at_risk['risk_level'] == 'Low']))

            # Filter
            risk_filter = st.multiselect(
                "Filter by risk level",
                options=['High', 'Medium', 'Low'],
                default=['High', 'Medium']
            )

            filtered_risk = at_risk[at_risk['risk_level'].isin(risk_filter)]

            # Display
            st.dataframe(
                filtered_risk[[
                    'name', 'department', 'tenure_days',
                    'risk_level', 'risk_factors'
                ]],
                use_container_width=True,
                hide_index=True
            )

            st.download_button(
                "📥 Download At-Risk List",
                filtered_risk.to_csv(index=False),
                "at_risk_employees.csv",
                "text/csv"
            )
        else:
            st.success("No employees currently flagged as at-risk!")

        # Forecast
        st.subheader("Turnover Forecast")
        forecast_data = predict_future_turnover(df, forecast_months=12)

        if forecast_data['forecast']:
            forecast_df = pd.DataFrame(forecast_data['forecast'])

            st.metric(
                "Expected Monthly Terminations",
                f"{forecast_data['avg_monthly_terminations']:.1f}",
                help=f"Based on {forecast_data['months_of_historical_data']} months of data"
            )

            st.line_chart(forecast_df.set_index('date')['expected_terminations'])

    # ==================== RAW DATA TAB ====================
    with tabs[4]:
        st.header("Raw Data")

        st.subheader("Employee Data")
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.download_button(
            "📥 Download Full Dataset",
            df.to_csv(index=False),
            "employee_data.csv",
            "text/csv"
        )

        # Data quality
        with st.expander("Data Quality Report"):
            st.write("**Missing Values:**")
            missing = df.isnull().sum()
            st.dataframe(missing[missing > 0], use_container_width=True)

            st.write("**Data Types:**")
            st.write(df.dtypes)


if __name__ == "__main__":
    main()
