import dash
from dash import dcc, html, Input, Output, dash_table
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Generate Sample Data
np.random.seed(42)
traders = ["Alice", "Bob", "Charlie", "David", "Eve"]
regions = ["US", "Europe", "Asia", "Australia", "South America"]
asset_types = ["Equity", "FX", "Commodity", "Bond", "Crypto"]
grades = ["Tier 1", "Tier 2", "Tier 3"]
instruments = ["EUR/USD", "Gold", "S&P500", "BTC/USD", "Brent Oil"]

data = pd.DataFrame({
    "Trader": np.random.choice(traders, 1000),
    "Region": np.random.choice(regions, 1000),
    "Asset_Type": np.random.choice(asset_types, 1000),
    "Counterparty_Grade": np.random.choice(grades, 1000),
    "Instrument": np.random.choice(instruments, 1000),
    "Trade_Type": np.random.choice(["Buy", "Sell"], 1000),
    "Amount": np.random.uniform(1000, 100000, 1000),
    "Trade_Price": np.random.uniform(50, 500, 1000),
    "Trade_Time": pd.date_range(start="2024-01-01", periods=1000, freq="H")
})

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Trader Activity Dashboard", style={"text-align": "center", "color": "#333"}),

    html.Div([
        html.Div([
            html.Label("Select Region:"),
            dcc.Dropdown(
                id="region-dropdown",
                options=[{"label": region, "value": region} for region in regions],
                value="US",
                clearable=False
            )
        ], style={"width": "20%", "display": "inline-block", "padding": "10px"}),

        html.Div([
            html.Label("Select Counterparty Grade:"),
            dcc.Dropdown(
                id="grade-dropdown",
                options=[{"label": grade, "value": grade} for grade in grades],
                value="Tier 1",
                clearable=False
            )
        ], style={"width": "20%", "display": "inline-block", "padding": "10px"}),

        html.Div([
            html.Label("Select Asset Type:"),
            dcc.Dropdown(
                id="asset-dropdown",
                options=[{"label": asset, "value": asset} for asset in asset_types],
                value="Equity",
                clearable=False
            )
        ], style={"width": "20%", "display": "inline-block", "padding": "10px"}),

        html.Div([
            html.Label("Adjust Trade Amount:"),
            dcc.Slider(
                id="amount-slider",
                min=data["Amount"].min(),
                max=data["Amount"].max(),
                step=5000,
                value=data["Amount"].max(),
                marks={i: f"${int(i)}" for i in range(1000, 100000, 20000)}
            )
        ], style={"width": "40%", "padding": "20px"})
    ], style={"display": "flex", "justify-content": "space-between"}),

    dcc.Graph(id="trade-volume-bar-chart"),
    dcc.Graph(id="trade-amount-line-chart"),
    dcc.Graph(id="trade-distribution-pie-chart"),

    html.Div([
        dcc.Graph(id="trade-heatmap", style={"width": "60%"}),
        html.Div([
            html.H4("Summary KPIs", style={"text-align": "center"}),
            html.Div(id="kpi-container", style={
                "padding": "20px", "border": "1px solid #ddd", "border-radius": "5px",
                "background-color": "#f9f9f9", "text-align": "center"
            })
        ], style={"width": "35%", "margin": "20px"})
    ], style={"display": "flex", "justify-content": "space-between"}),

    html.H4("Trade Data Table", style={"text-align": "center"}),
    dash_table.DataTable(
        id="trade-table",
        columns=[{"name": col, "id": col} for col in data.columns],
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left"},
        page_size=10
    )
])

# Callbacks
@app.callback(
    [Output("trade-volume-bar-chart", "figure"),
     Output("trade-amount-line-chart", "figure"),
     Output("trade-distribution-pie-chart", "figure"),
     Output("trade-heatmap", "figure"),
     Output("kpi-container", "children"),
     Output("trade-table", "data")],
    [Input("region-dropdown", "value"),
     Input("grade-dropdown", "value"),
     Input("asset-dropdown", "value"),
     Input("amount-slider", "value")]
)
def update_dashboard(region, grade, asset_type, amount):
    filtered_data = data[
        (data["Region"] == region) &
        (data["Counterparty_Grade"] == grade) &
        (data["Asset_Type"] == asset_type) &
        (data["Amount"] <= amount)
    ]

    # Bar Chart
    bar_fig = px.bar(
        filtered_data, x="Instrument", y="Amount", color="Trade_Type",
        title="Trade Volume by Instrument"
    )

    # Line Chart
    line_fig = px.line(
        filtered_data, x="Trade_Time", y="Amount",
        title="Trade Amount Over Time"
    )

    # Pie Chart
    pie_fig = px.pie(
        filtered_data, names="Trade_Type", values="Amount",
        title="Trade Distribution by Type"
    )

    # Heatmap
    heatmap_data = filtered_data.groupby(["Region", "Asset_Type"])["Amount"].sum().reset_index()
    heatmap_fig = px.density_heatmap(
        heatmap_data, x="Region", y="Asset_Type", z="Amount",
        title="Trade Volume Heatmap"
    )

    # KPIs
    total_trades = len(filtered_data)
    avg_amount = filtered_data["Amount"].mean()
    active_trader = filtered_data["Trader"].value_counts().idxmax()
    kpis = html.Div([
        html.P(f"Total Trades: {total_trades}"),
        html.P(f"Average Amount: ${avg_amount:,.2f}"),
        html.P(f"Most Active Trader: {active_trader}")
    ])

    # Data Table
    table_data = filtered_data.to_dict("records")

    return bar_fig, line_fig, pie_fig, heatmap_fig, kpis, table_data

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
