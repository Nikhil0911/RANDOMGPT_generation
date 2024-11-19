import dash
from dash import dcc, html, Input, Output
import pandas as pd
import numpy as np

# Improved data generation
np.random.seed(42)

# Define regions, assets, sub-assets, tenors, and counterparty types
regions = ['US', 'UK', 'APAC', 'EMEA', 'LATAM']
assets = ['FX', 'Commodity', 'Equity', 'Rates', 'Credit']
sub_assets = ['FX Swaps', 'FX Options', 'Oil', 'Gold', 'Equity Derivatives']
tenors = ['Short', 'Medium', 'Long']
counterparty_types = ['Street', 'Internal']

# Generate sample data
data = {
    'Region': np.random.choice(regions, 500),
    'Asset': np.random.choice(assets, 500),
    'Sub-Asset': np.random.choice(sub_assets, 500),
    'Tenor': np.random.choice(tenors, 500),
    'Amount': np.random.lognormal(mean=6, sigma=0.5, size=500),  # Log-normal distribution for Amount
    'Threshold': np.random.randint(50, 200, 500),
    'Counterparty': [f'CP-{i}' for i in np.random.randint(1, 101, 500)],
    'Counterparty Type': np.random.choice(counterparty_types, 500),
    'Alerts': np.random.randint(0, 15, 500),
    'Month': ['November'] * 500
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
    street_count = len(filtered_df[filtered_df['Counterparty Type'] == 'Street'])
    internal_count = len(filtered_df[filtered_df['Counterparty Type'] == 'Internal'])
    metrics = [
        html.P(f"Month: {filtered_df['Month'].iloc[0]}"),
        html.P(f"Current Threshold: ${filtered_df['Threshold'].mean():.2f}"),
        html.P(f"Count of Trades: {len(filtered_df)}"),
        html.P(f"Street Counterparties: {street_count}"),
        html.P(f"Internal Counterparties: {internal_count}")
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
