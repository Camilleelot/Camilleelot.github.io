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
    plot_yearly_costs, plot_survival_curve, plot_case_distribution,
    plot_case_by_role_heatmap, plot_voluntary_by_case, plot_sankey_flow,
    plot_role_comparison, plot_employment_type_by_case
)
from predictive import (
    identify_high_risk_tenure_periods, flag_at_risk_employees,
    predict_future_turnover, analyze_seasonal_patterns,
    calculate_turnover_velocity
)
from case_analysis import (
    assign_case_type, calculate_case_distribution, calculate_case_by_role,
    calculate_voluntary_by_case, identify_high_risk_roles,
    generate_case_insights, create_sankey_data, calculate_employment_type_by_case
)


# Page config
st.set_page_config(
    page_title="NGO Turnover Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


def show_landing_page():
    """Display landing page with setup instructions"""

    # Custom CSS for Tufte-style aesthetics
    st.markdown("""
    <style>
    .big-title {
        font-size: 2.5rem;
        font-weight: 300;
        letter-spacing: -0.02em;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        font-weight: 300;
        color: #666;
        font-style: italic;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: 400;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 1px solid #ccc;
    }
    .math-notation {
        font-family: 'Courier New', monospace;
        background: #f5f5f5;
        padding: 2px 6px;
        border-radius: 3px;
        font-size: 0.95em;
    }
    .sidenote {
        font-size: 0.9rem;
        color: #666;
        font-style: italic;
        padding-left: 1rem;
        border-left: 2px solid #ddd;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Hero section
    st.markdown('<div class="big-title">Turnover Analysis Tool</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">A formal approach to understanding organizational retention</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Introduction
    st.markdown("""
    ### The Problem

    Let *T* denote the set of all employees and *T*₀ ⊂ *T* denote those who have terminated.
    The turnover rate *r* is defined as:

    <div style='text-align: center; font-size: 1.1em; margin: 1.5rem 0;'>
    <i>r</i> = |<i>T</i>₀| / |<i>T</i>| × 100
    </div>

    For nonprofits, *r* ∈ [40%, 65%] is typical. But this single number obscures the underlying dynamics:
    **when** do people leave? **why** do they leave? **what** does it cost?
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sidenote">
    <b>Note:</b> Traditional HR reporting treats turnover as a scalar.
    This tool treats it as a temporal distribution with causal structure.
    </div>
    """, unsafe_allow_html=True)

    # What this does
    st.markdown('<div class="section-header">What This Tool Does</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **Case-Based Analysis**
        Categorizes terminations ∀*e* ∈ *T*₀ by tenure *t*:

        - **Case 0**: *t* = 0 (never started)
        - **Case 1**: 0 < *t* < 90 days
        - **Case 2**: 90 ≤ *t* < 365 days
        - **Case 3**: 1 ≤ *t* < 3 years
        - **Case 4**: 3 ≤ *t* < 5 years
        - **Case 5**: *t* ≥ 5 years

        **Cohort Retention**
        Tracks survival function *S*(*t*) by hire cohort

        **Flow Analysis**
        Sankey diagrams: Department → Role → Outcome
        """)

    with col2:
        st.markdown("""
        **Cost Modeling**
        Total cost *C* per termination:

        *C* = *S* × (0.20 + 0.10 + 0.50)
        where *S* = annual salary

        - Recruitment: 20%
        - Training: 10%
        - Productivity loss: 50%

        **Predictive Risk**
        Flags employees *e* ∈ *T* where *P*(terminate) > *θ*

        **Temporal Patterns**
        Seasonal analysis, velocity, trends
        """)

    # Setup instructions
    st.markdown('<div class="section-header">Setup Instructions</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="sidenote">
    <b>First time doing this?</b> Don't forget to read the manul! →
    (A distinguished gentleman in a top hat will guide you)
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### For the Non-Programmer

    **Axiom 1:** You need data in Excel format
    **Axiom 2:** The sidebar accepts `.xlsx` or `.xls` files
    **Axiom 3:** Therefore, export → upload → analyze

    #### Step-by-Step (truly from scratch)

    **1. Prepare Your Data**

    You need a spreadsheet with these columns:

    | employee_id | name | hire_date | termination_date | department | role | salary |
    |-------------|------|-----------|------------------|------------|------|--------|
    | 2001 | Jordan Mitchell | 2023-02-10 | | Programs | Coordinator | 51000 |
    | 2002 | Taylor Brooks | 2023-11-20 | 2024-01-15 | Operations | Support Worker | 39000 |

    - **hire_date**: When they started (YYYY-MM-DD)
    - **termination_date**: When they left (empty if still employed)
    - **Optional**: `termination_reason` (Voluntary/Involuntary), `employment_type` (Full-time/Part-time)

    **2. Upload**

    Look to the left sidebar → "Upload your Excel file" → Click → Select file → Done

    **3. Explore**

    Six tabs await you:
    - **Overview**: High-level metrics
    - **Cohort Analysis**: Who stays, who goes, when
    - **Case Analysis**: The six tenure windows (this is where the magic happens)
    - **Cost Analysis**: Financial impact
    - **Risk Assessment**: Who might leave next
    - **Raw Data**: Your data table

    **4. Try Sample Data First**

    Check the box "Use sample data" in the sidebar to see how it works before uploading your own.
    """)

    # Philosophy section
    st.markdown('<div class="section-header">Philosophical Foundation</div>', unsafe_allow_html=True)

    st.markdown("""
    This tool embodies three principles:

    **Clarity** ≡ showing the data without distortion
    **Precision** ≡ measuring what matters, not what's easy
    **Utility** ≡ insights → decisions → actions

    *Turnover is not failure. Turnover is information.*

    The question is not "how do we reduce turnover to zero?" (impossible, undesirable).
    The question is "what is turnover telling us?" (actionable, valuable).
    """)

    st.markdown("---")

    # Call to action
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("""
        **To begin:** Upload data via the sidebar, or check "Use sample data" to explore with synthetic examples.
        """)

    # Download template
    template = create_sample_template()
    st.download_button(
        "📥 Download Template Spreadsheet",
        template.to_csv(index=False),
        "turnover_template.csv",
        "text/csv",
        help="Download a template with the correct format"
    )


def show_manul_help():
    """Display the manul help page"""
    st.markdown("""
    <style>
    .manul-container {
        text-align: center;
        padding: 2rem;
    }
    .manul-title {
        font-size: 2rem;
        font-weight: 300;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="manul-title">📖 Read the Manul</div>', unsafe_allow_html=True)

    st.markdown("""
    ### First time doing this?

    **Don't forget to read the manul!**
    """)

    # Placeholder for manul image
    st.info("""
    🎩 **[Image placeholder: Distinguished manul in top hat goes here]**

    *A wise manul once said: "The best way to understand turnover is to visualize it.
    The second best way is to read documentation. I recommend both."*
    """)

    st.markdown("---")

    st.markdown("""
    ### Quick Guide

    **What is a manul?**
    A small wild cat (*Otocolobus manul*) known for its wisdom and excellent taste in haberdashery.

    **What should I do first?**
    1. Check "Use sample data" in the sidebar
    2. Click through the tabs to see what's possible
    3. Export your own data from your HRIS
    4. Upload and explore

    **I'm stuck. What now?**
    - Check that your date columns are formatted as YYYY-MM-DD
    - Make sure employee_id, name, and hire_date are present
    - Look at the sample data format (download template button on main page)

    **Where do I find my organization's data?**
    Most HRIS systems (BambooHR, Rippling, Gusto, etc.) have an "Export" button.
    Look for "Employee Report" or "Termination Report" in your admin panel.
    """)


def main():
    # Check if showing manul help
    if st.session_state.get('show_manul', False):
        show_manul_help()
        if st.button("← Back to Main"):
            st.session_state['show_manul'] = False
            st.rerun()
        st.stop()

    st.title("📊 NGO Turnover Analysis Tool")
    st.markdown("Transform your employee data into actionable insights")

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")

        # Help link
        if st.button("🎩 Read the Manul", help="First time? Start here!"):
            st.session_state['show_manul'] = True
            st.rerun()

        st.markdown("---")

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
        # ==================== LANDING PAGE ====================
        show_landing_page()
        st.stop()

    # Main dashboard
    tabs = st.tabs([
        "📈 Overview",
        "👥 Cohort Analysis",
        "🔍 Case Analysis",
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

    # ==================== CASE ANALYSIS TAB ====================
    with tabs[2]:
        st.header("Case Analysis")
        st.markdown("Understand **when** and **why** employees leave through case-based tenure analysis")

        # Assign case types
        df_with_cases = assign_case_type(df, only_terminated=True)

        # Generate insights
        insights = generate_case_insights(df_with_cases)

        # Display key insights
        if insights:
            st.subheader("🔍 Key Insights")
            for insight in insights:
                st.info(insight)

        st.markdown("---")

        # Case distribution
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Case Distribution")
            case_dist = calculate_case_distribution(df_with_cases)
            if not case_dist.empty:
                fig = plot_case_distribution(case_dist)
                st.plotly_chart(fig, use_container_width=True)

                # Show case definitions
                with st.expander("📖 Case Definitions"):
                    for _, row in case_dist.iterrows():
                        st.markdown(f"**{row['case_type']} - {row['case_name']}**")
                        st.caption(row['description'])
                        st.caption(f"Count: {row['count']:.0f} ({row['percentage']:.1f}%)")
                        st.markdown("---")
            else:
                st.info("No termination data available")

        with col2:
            st.subheader("Voluntary vs Involuntary by Case")
            if 'termination_reason' in df_with_cases.columns:
                vol_by_case = calculate_voluntary_by_case(df_with_cases)
                if not vol_by_case.empty:
                    fig = plot_voluntary_by_case(vol_by_case)
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No data available")
            else:
                st.warning("Add 'termination_reason' column to your data for this analysis")

        # Sankey diagram
        st.subheader("Employee Flow: Department → Role → Outcome")
        st.caption("Visualize how employees flow from departments through roles to different outcomes")

        sankey_data = create_sankey_data(df_with_cases)
        if sankey_data['labels']:
            fig = plot_sankey_flow(sankey_data)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Need department and role data for flow diagram")

        # Role-specific case analysis
        st.subheader("Role Distribution Across Cases")

        if 'role' in df_with_cases.columns:
            role_case = calculate_case_by_role(df_with_cases, top_n=10)
            if not role_case.empty:
                fig = plot_case_by_role_heatmap(role_case)
                st.plotly_chart(fig, use_container_width=True)

                st.dataframe(role_case, use_container_width=True)
            else:
                st.info("No role data available")

            # Deep dive on specific case
            st.markdown("---")
            st.subheader("Case Deep Dive")

            selected_case = st.selectbox(
                "Select a case to analyze",
                options=['Case 0', 'Case 1', 'Case 2', 'Case 3', 'Case 4', 'Case 5'],
                index=2  # Default to Case 2 (biggest window typically)
            )

            case_details = case_dist[case_dist['case_type'] == selected_case]
            if not case_details.empty:
                case_name = case_details['case_name'].values[0]

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Case Name", case_name)
                with col2:
                    st.metric("Terminations", f"{case_details['count'].values[0]:.0f}")
                with col3:
                    st.metric("% of Total", f"{case_details['percentage'].values[0]:.1f}%")

                # Top roles in this case
                role_risk = identify_high_risk_roles(df_with_cases, case_window=selected_case)
                if not role_risk.empty:
                    fig = plot_role_comparison(role_risk, case_name)
                    st.plotly_chart(fig, use_container_width=True)

                    st.dataframe(
                        role_risk[['role', 'count', 'pct_of_case', 'pct_of_all_terminations']],
                        use_container_width=True,
                        hide_index=True
                    )
        else:
            st.warning("Add 'role' column to your data for detailed role analysis")

        # Employment type analysis
        if 'employment_type' in df_with_cases.columns:
            st.markdown("---")
            st.subheader("Employment Type by Case")

            emp_type_case = calculate_employment_type_by_case(df_with_cases)
            if not emp_type_case.empty:
                fig = plot_employment_type_by_case(emp_type_case)
                st.plotly_chart(fig, use_container_width=True)

                st.caption("💡 **Insight**: Part-time or hourly roles often show higher early attrition (Case 1-2)")

    # ==================== COST ANALYSIS TAB ====================
    with tabs[3]:
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
    with tabs[4]:
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
    with tabs[5]:
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
