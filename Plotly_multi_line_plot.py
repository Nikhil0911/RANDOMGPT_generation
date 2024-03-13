import plotly.express as px

# Assuming df is your DataFrame
fig = px.line(df, x=df.columns[1:], y=df.columns[2:], color='instrument', labels={'x': 'Features', 'y': 'Scores'},
              title='Company Trends Across Features', line_shape='linear')

# Save the plot
fig.write_image("plotly_plot.png")
