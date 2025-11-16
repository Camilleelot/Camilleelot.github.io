"""
Visualization module
Creates interactive charts for the dashboard
"""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


def plot_cohort_retention(retention_df: pd.DataFrame) -> go.Figure:
    """
    Create cohort retention heatmap

    Args:
        retention_df: Output from calculate_cohort_retention()

    Returns:
        Plotly figure
    """
    # Pivot for heatmap
    pivot = retention_df.pivot(
        index='cohort',
        columns='months',
        values='retention_rate'
    )

    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale='RdYlGn',
        text=pivot.values.round(1),
        texttemplate='%{text}%',
        textfont={"size": 10},
        colorbar=dict(title="Retention %")
    ))

    fig.update_layout(
        title="Cohort Retention Rates Over Time",
        xaxis_title="Months Since Hire",
        yaxis_title="Hire Cohort",
        height=500,
        yaxis={'autorange': 'reversed'}
    )

    return fig


def plot_turnover_trend(turnover_df: pd.DataFrame) -> go.Figure:
    """
    Create turnover rate trend line chart

    Args:
        turnover_df: Output from calculate_turnover_by_period()

    Returns:
        Plotly figure
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=turnover_df['period'],
        y=turnover_df['turnover_rate'],
        mode='lines+markers',
        name='Turnover Rate',
        line=dict(color='#e74c3c', width=3),
        marker=dict(size=8)
    ))

    # Add average line
    avg_rate = turnover_df['turnover_rate'].mean()
    fig.add_hline(
        y=avg_rate,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"Average: {avg_rate:.1f}%",
        annotation_position="right"
    )

    fig.update_layout(
        title="Turnover Rate Over Time (Annualized)",
        xaxis_title="Period",
        yaxis_title="Annual Turnover Rate (%)",
        height=400,
        hovermode='x unified'
    )

    return fig


def plot_department_comparison(dept_df: pd.DataFrame) -> go.Figure:
    """
    Create department turnover comparison chart

    Args:
        dept_df: Output from calculate_department_turnover()

    Returns:
        Plotly figure
    """
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=dept_df['department'],
        y=dept_df['turnover_rate'],
        text=dept_df['turnover_rate'].round(1),
        texttemplate='%{text}%',
        textposition='outside',
        marker_color='#3498db'
    ))

    # Add benchmark line (industry average ~20-25% for nonprofits)
    fig.add_hline(
        y=22,
        line_dash="dash",
        line_color="red",
        annotation_text="NGO Sector Avg (~22%)",
        annotation_position="right"
    )

    fig.update_layout(
        title="Turnover Rate by Department",
        xaxis_title="Department",
        yaxis_title="Turnover Rate (%)",
        height=400,
        showlegend=False
    )

    return fig


def plot_tenure_distribution(tenure_df: pd.DataFrame) -> go.Figure:
    """
    Create tenure distribution chart

    Args:
        tenure_df: Output from calculate_tenure_distribution()

    Returns:
        Plotly figure
    """
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=tenure_df['tenure_bucket'],
        y=tenure_df['count'],
        text=tenure_df['percentage'].round(1),
        texttemplate='%{text}%',
        textposition='outside',
        marker_color='#9b59b6'
    ))

    fig.update_layout(
        title="When Do Employees Leave? (Tenure Distribution)",
        xaxis_title="Tenure at Termination",
        yaxis_title="Number of Employees",
        height=400,
        showlegend=False
    )

    return fig


def plot_cost_breakdown(cost_summary: dict) -> go.Figure:
    """
    Create cost breakdown pie chart

    Args:
        cost_summary: Output from calculate_aggregate_costs()

    Returns:
        Plotly figure
    """
    labels = ['Recruitment', 'Training', 'Productivity Loss']
    values = [
        cost_summary['total_recruitment_cost'],
        cost_summary['total_training_cost'],
        cost_summary['total_productivity_loss']
    ]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.3,
        marker_colors=['#e74c3c', '#f39c12', '#3498db']
    )])

    fig.update_layout(
        title="Turnover Cost Breakdown",
        height=400,
        annotations=[dict(text='Total Cost', x=0.5, y=0.5, font_size=16, showarrow=False)]
    )

    return fig


def plot_cost_by_department(dept_cost_df: pd.DataFrame) -> go.Figure:
    """
    Create department cost comparison

    Args:
        dept_cost_df: Output from calculate_costs_by_department()

    Returns:
        Plotly figure
    """
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=dept_cost_df['department'],
        y=dept_cost_df['total_cost'],
        text=['$' + f"{x:,.0f}" for x in dept_cost_df['total_cost']],
        textposition='outside',
        marker_color='#e74c3c'
    ))

    fig.update_layout(
        title="Total Turnover Costs by Department",
        xaxis_title="Department",
        yaxis_title="Total Cost ($)",
        height=400,
        showlegend=False
    )

    return fig


def plot_yearly_costs(yearly_cost_df: pd.DataFrame) -> go.Figure:
    """
    Create stacked bar chart of costs by year

    Args:
        yearly_cost_df: Output from calculate_costs_by_year()

    Returns:
        Plotly figure
    """
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Recruitment',
        x=yearly_cost_df['year'],
        y=yearly_cost_df['recruitment_cost'],
        marker_color='#e74c3c'
    ))

    fig.add_trace(go.Bar(
        name='Training',
        x=yearly_cost_df['year'],
        y=yearly_cost_df['training_cost'],
        marker_color='#f39c12'
    ))

    fig.add_trace(go.Bar(
        name='Productivity Loss',
        x=yearly_cost_df['year'],
        y=yearly_cost_df['productivity_loss'],
        marker_color='#3498db'
    ))

    fig.update_layout(
        title="Annual Turnover Costs",
        xaxis_title="Year",
        yaxis_title="Cost ($)",
        barmode='stack',
        height=400
    )

    return fig


def plot_survival_curve(survival_df: pd.DataFrame) -> go.Figure:
    """
    Create employee survival curve

    Args:
        survival_df: Output from calculate_survival_curve()

    Returns:
        Plotly figure
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=survival_df['month'],
        y=survival_df['survival_rate'],
        mode='lines',
        name='Survival Rate',
        line=dict(color='#2ecc71', width=3),
        fill='tozeroy',
        fillcolor='rgba(46, 204, 113, 0.2)'
    ))

    # Add key milestones
    milestones = [3, 6, 12, 24]
    for m in milestones:
        if m in survival_df['month'].values:
            rate = survival_df[survival_df['month'] == m]['survival_rate'].values[0]
            fig.add_annotation(
                x=m, y=rate,
                text=f"{m}mo: {rate:.0f}%",
                showarrow=True,
                arrowhead=2
            )

    fig.update_layout(
        title="Employee Retention Curve",
        xaxis_title="Months Since Hire",
        yaxis_title="% Still Employed",
        height=400,
        yaxis=dict(range=[0, 105])
    )

    return fig


def create_metric_card(title: str, value: str, delta: str = None) -> dict:
    """
    Create a metric card for display

    Args:
        title: Metric name
        value: Main value to display
        delta: Optional change indicator

    Returns:
        Dictionary with metric info
    """
    return {
        'title': title,
        'value': value,
        'delta': delta
    }


def plot_case_distribution(case_df: pd.DataFrame) -> go.Figure:
    """
    Create bar chart of terminations by case type

    Args:
        case_df: Output from calculate_case_distribution()

    Returns:
        Plotly figure
    """
    # Import case definitions for colors
    from case_analysis import CASE_DEFINITIONS

    colors = [CASE_DEFINITIONS.get(case, {}).get('color', '#95a5a6')
              for case in case_df['case_type']]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=case_df['case_type'],
        y=case_df['percentage'],
        text=case_df['percentage'].round(1),
        texttemplate='%{text}%',
        textposition='outside',
        marker_color=colors,
        hovertemplate='<b>%{x}</b><br>' +
                      '%{customdata[0]}<br>' +
                      'Count: %{customdata[1]}<br>' +
                      'Percentage: %{y:.1f}%<extra></extra>',
        customdata=case_df[['case_name', 'count']].values
    ))

    fig.update_layout(
        title="Termination Distribution by Case Type",
        xaxis_title="Case Type",
        yaxis_title="Percentage of All Terminations (%)",
        height=450,
        showlegend=False
    )

    return fig


def plot_case_by_role_heatmap(role_case_df: pd.DataFrame) -> go.Figure:
    """
    Create heatmap showing role x case distribution

    Args:
        role_case_df: Output from calculate_case_by_role()

    Returns:
        Plotly figure
    """
    # Exclude total_terminations column for heatmap
    heatmap_data = role_case_df.drop('total_terminations', axis=1, errors='ignore')

    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='YlOrRd',
        text=heatmap_data.values.round(1),
        texttemplate='%{text}%',
        textfont={"size": 10},
        colorbar=dict(title="% of Role")
    ))

    fig.update_layout(
        title="Role Distribution Across Case Types",
        xaxis_title="Case Type",
        yaxis_title="Role",
        height=max(400, len(heatmap_data) * 30),
        yaxis={'autorange': 'reversed'}
    )

    return fig


def plot_voluntary_by_case(vol_case_df: pd.DataFrame) -> go.Figure:
    """
    Create stacked bar chart of voluntary vs involuntary by case

    Args:
        vol_case_df: Output from calculate_voluntary_by_case()

    Returns:
        Plotly figure
    """
    fig = go.Figure()

    fig.add_trace(go.Bar(
        name='Voluntary',
        x=vol_case_df['case_type'],
        y=vol_case_df['voluntary_count'],
        marker_color='#3498db',
        text=vol_case_df['voluntary_pct'].round(1),
        texttemplate='%{text}%',
        textposition='inside'
    ))

    fig.add_trace(go.Bar(
        name='Involuntary',
        x=vol_case_df['case_type'],
        y=vol_case_df['involuntary_count'],
        marker_color='#e74c3c',
        text=vol_case_df['involuntary_pct'].round(1),
        texttemplate='%{text}%',
        textposition='inside'
    ))

    fig.update_layout(
        title="Voluntary vs Involuntary Terminations by Case",
        xaxis_title="Case Type",
        yaxis_title="Number of Terminations",
        barmode='stack',
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig


def plot_sankey_flow(sankey_data: dict) -> go.Figure:
    """
    Create Sankey diagram showing Department → Role → Outcome flow

    Args:
        sankey_data: Output from create_sankey_data()

    Returns:
        Plotly figure
    """
    # Define colors for different node types
    node_colors = []
    for label in sankey_data['labels']:
        if 'Dept:' in label:
            node_colors.append('#3498db')  # Blue for departments
        elif 'Role:' in label:
            node_colors.append('#95a5a6')  # Gray for roles
        elif 'Still Employed' in label:
            node_colors.append('#2ecc71')  # Green for active
        else:  # Cases
            node_colors.append('#e74c3c')  # Red for terminations

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="white", width=0.5),
            label=sankey_data['labels'],
            color=node_colors
        ),
        link=dict(
            source=sankey_data['source'],
            target=sankey_data['target'],
            value=sankey_data['value']
        )
    )])

    fig.update_layout(
        title="Employee Flow: Department → Role → Outcome",
        font_size=10,
        height=800
    )

    return fig


def plot_role_comparison(role_risk_df: pd.DataFrame, case_name: str) -> go.Figure:
    """
    Create bar chart comparing roles within a specific case

    Args:
        role_risk_df: Output from identify_high_risk_roles()
        case_name: Name of the case being analyzed

    Returns:
        Plotly figure
    """
    top_10 = role_risk_df.head(10)

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=top_10['role'],
        y=top_10['count'],
        text=top_10['pct_of_case'].round(1),
        texttemplate='%{text}% of case',
        textposition='outside',
        marker_color='#e67e22'
    ))

    fig.update_layout(
        title=f"Top Roles in {case_name}",
        xaxis_title="Role",
        yaxis_title="Number of Terminations",
        height=450,
        showlegend=False,
        xaxis={'tickangle': -45}
    )

    return fig


def plot_employment_type_by_case(emp_case_df: pd.DataFrame) -> go.Figure:
    """
    Create stacked bar showing employment type distribution across cases

    Args:
        emp_case_df: Output from calculate_employment_type_by_case()

    Returns:
        Plotly figure
    """
    # Exclude total_count for stacking
    plot_data = emp_case_df.drop('total_count', axis=1, errors='ignore')

    fig = go.Figure()

    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']

    for idx, emp_type in enumerate(plot_data.index):
        fig.add_trace(go.Bar(
            name=emp_type,
            x=plot_data.columns,
            y=plot_data.loc[emp_type],
            marker_color=colors[idx % len(colors)]
        ))

    fig.update_layout(
        title="Employment Type Distribution Across Cases",
        xaxis_title="Case Type",
        yaxis_title="Percentage (%)",
        barmode='stack',
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    return fig
