import plotly.graph_objects as go
from plotly.graph_objects import Layout
fanduel_colors = {
    'dark-blue-grey': '#445058',
    'medium-blue-grey': '#F0F3F8',
    'superdark-blue': '#1F375B',
    'dark-blue': '#1381E0',
    'medium-blue': '#0E67B3',
    'light-blue': '#818E95',
    'red': '#E44242',
    'dark-red': '#BF2D2D',
    'white': '#FFFFFF',
    'light-grey': '#CFD6DB'
}

fanduel_title = {
    'font': {
        'size': 16,
        'color': fanduel_colors['white']}
}

fanduel_xaxis = {
    'showgrid': False,
    'linecolor': fanduel_colors['light-grey'],
    'color': fanduel_colors['light-grey'],
    'tickangle': 315,
    'titlefont': {
        'size': 12,
        'color': fanduel_colors['light-grey']},
    'tickfont': {
        'size': 11,
        'color': fanduel_colors['light-grey']},
    'zeroline': False
}

fanduel_yaxis = {
    'showgrid': True,
    'color': fanduel_colors['light-grey'],
    'gridwidth': 0.5,
    'gridcolor': fanduel_colors['dark-blue'],
    'linecolor': fanduel_colors['light-grey'],
    'titlefont': {
        'size': 12,
        'color': fanduel_colors['light-grey']},
    'tickfont': {
        'size': 11,
        'color': fanduel_colors['light-grey']},
    'zeroline': False
}

fanduel_font_family = 'Proxima Nova'

fanduel_legend = {
    'orientation': 'h',
    'yanchor': 'bottom',
    'y': 1.01,
    'xanchor': 'right',
    'x': 1.05,
    'font': {'size': 9, 'color': fanduel_colors['light-grey']}
}  # Legend will be on the top right, above the graph, horizontally

# Set top margin to in case there is a legend
fanduel_margins = {'l': 5, 'r': 5, 't': 45, 'b': 15}

fanduel_layout = Layout(
    font={'family': fanduel_font_family},
    title=fanduel_title,
    title_x=0.5,  # Align chart title to center
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=fanduel_xaxis,
    yaxis=fanduel_yaxis,
    height=270,
    legend=fanduel_legend,
    margin=fanduel_margins
)
