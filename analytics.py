import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_monthly_trend_chart(monthly_data):
    df_reset = monthly_data.reset_index()
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df_reset['month'],
        y=df_reset['Income'],
        name='Income',
        line=dict(color='green')
    ))
    
    fig.add_trace(go.Scatter(
        x=df_reset['month'],
        y=df_reset['Expense'],
        name='Expense',
        line=dict(color='red')
    ))
    
    fig.add_trace(go.Scatter(
        x=df_reset['month'],
        y=df_reset['Balance'],
        name='Balance',
        line=dict(color='blue')
    ))
    
    fig.update_layout(
        title='Monthly Financial Trend',
        xaxis_title='Month',
        yaxis_title='Amount',
        hovermode='x unified'
    )
    return fig

def create_expense_category_chart(category_data):
    fig = px.pie(
        values=category_data.values,
        names=category_data.index,
        title='Expense Distribution by Category'
    )
    return fig
