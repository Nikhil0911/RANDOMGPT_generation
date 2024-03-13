import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

app = dash.Dash(__name__)

# Assuming df is your DataFrame
fig = px.line(df, x=df.columns[1:], y=df.columns[2:], color='instrument', labels={'x': 'Features', 'y': 'Scores'},
              title='Company Trends Across Features', line_shape='linear')

app.layout = html.Div([
    dcc.Graph(figure=fig),
])

# Save the plot
fig.write_image("dash_plot.png")

if __name__ == '__main__':
    app.run_server(debug=True)
 
