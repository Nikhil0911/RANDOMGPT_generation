import dash
from dash import dcc, html, Input, Output
import pandas as pd
import numpy as np

# Simulate sample data
data = {
    'Region': ['US', 'UK', 'APAC', 'EMEA', 'LATAM'] * 20,
    'Asset': ['FX', 'Commodity', 'Equity', 'Rates', 'Credit'] * 20,
    'Sub-Asset': ['FX Swaps', 'FX Options', 'Oil', 'Gold', 'Equity Derivatives'] * 20,
    'Tenor': ['Short', 'Medium', 'Long'] * 33 + ['Short'],
    'Amount': np.random.randint(100, 1000, 100),
    'Threshold': np.random.randint(50, 200, 100),
    'Counterparty': [f'CP-{i}' for i in range(1, 21)] * 5,
    'Alerts': np.random.randint(0, 10, 100),
    'Month': ['November'] * 100
}
df = pd.DataFrame(data)

# Initialize Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Trader Dashboard", style={'textAlign': 'center'}),

    # Dropdown filters
    html.Div([
        html.Label("Select Asset:"),
        dcc.Dropdown(
            id='asset-dropdown',
            options=[{'label': asset, 'value': asset} for asset in df['Asset'].unique()],
            value=df['Asset'].unique()[0]
        ),
        html.Label("Select Sub-Asset:"),
        dcc.Dropdown(
            id='sub-asset-dropdown',
            options=[{'label': sub_asset, 'value': sub_asset} for sub_asset in df['Sub-Asset'].unique()],
            value=df['Sub-Asset'].unique()[0]
        ),
        html.Label("Select Tenor:"),
        dcc.Dropdown(
            id='tenor-dropdown',
            options=[{'label': tenor, 'value': tenor} for tenor in df['Tenor'].unique()],
            value=df['Tenor'].unique()[0]
        ),
    ], style={'width': '25%', 'display': 'inline-block', 'verticalAlign': 'top'}),

    # Static and dynamic metrics
    html.Div([
        html.H3("Key Metrics"),
        html.Div(id='metrics-div', style={'fontSize': '18px'})
    ], style={'width': '70%', 'display': 'inline-block', 'paddingLeft': '20px'}),

    # Bar chart for alerts count
    html.Div([
        html.H3("Alerts Count by Region"),
        dcc.Graph(id='alerts-bar-chart')
    ]),

    # Histogram for amount traded distribution
    html.Div([
        html.H3("Amount Traded Distribution by Region"),
        dcc.Graph(id='amount-histogram')
    ])
])

# Callbacks for dynamic updates
@app.callback(
    [Output('metrics-div', 'children'),
     Output('alerts-bar-chart', 'figure'),
     Output('amount-histogram', 'figure')],
    [Input('asset-dropdown', 'value'),
     Input('sub-asset-dropdown', 'value'),
     Input('tenor-dropdown', 'value')]
)
def update_dashboard(selected_asset, selected_sub_asset, selected_tenor):
    # Filter data based on selections
    filtered_df = df[
        (df['Asset'] == selected_asset) &
        (df['Sub-Asset'] == selected_sub_asset) &
        (df['Tenor'] == selected_tenor)
    ]

    # Metrics
    metrics = [
        html.P(f"Month: {filtered_df['Month'].iloc[0]}"),
        html.P(f"Current Threshold: ${filtered_df['Threshold'].mean():.2f}"),
        html.P(f"Count of Trades: {len(filtered_df)}"),
        html.P(f"Count of Counterparties: {filtered_df['Counterparty'].nunique()}")
    ]

    # Alerts Count by Region
    alerts_by_region = filtered_df.groupby('Region')['Alerts'].sum().reset_index()
    alerts_fig = {
        'data': [
            {'x': alerts_by_region['Region'], 'y': alerts_by_region['Alerts'], 'type': 'bar', 'name': 'Alerts'}
        ],
        'layout': {'title': 'Alerts Count by Region'}
    }

    # Amount Traded Distribution by Region
    amount_by_region = filtered_df.groupby('Region')['Amount'].sum().reset_index()
    amount_fig = {
        'data': [
            {'x': amount_by_region['Region'], 'y': amount_by_region['Amount'], 'type': 'bar', 'name': 'Amount'}
        ],
        'layout': {'title': 'Amount Traded Distribution by Region'}
    }

    return metrics, alerts_fig, amount_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
