from bokeh.plotting import figure, output_file, show
from bokeh.palettes import Category10
from bokeh.models import Legend

# Assuming df is your DataFrame
output_file("company_trends.html")

p = figure(title='Company Trends Across Features', x_axis_label='Features', y_axis_label='Scores')

for i, (_, row) in enumerate(df.iterrows()):
    p.line(row.index[1:], row.values[1:], line_width=2, legend_label=row['instrument'],
           line_color=Category10[10][i % 10])

p.legend.title = 'Companies'
p.legend.label_text_font_size = '10pt'
p.legend.label_height = 10
p.legend.glyph_height = 15
p.legend.spacing = 2
p.legend.click_policy = 'hide'

# Save the plot
show(p)
