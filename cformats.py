import plotly.graph_objects as go
from plotly.graph_objects import Layout
account_colors = {
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

account_title = {
    'font': {
        'size': 16,
        'color': account_colors['white']}
}

account_xaxis = {
    'showgrid': False,
    'linecolor': account_colors['light-grey'],
    'color': account_colors['light-grey'],
    'tickangle': 315,
    'titlefont': {
        'size': 12,
        'color': account_colors['light-grey']},
    'tickfont': {
        'size': 11,
        'color': account_colors['light-grey']},
    'zeroline': False
}

account_yaxis = {
    'showgrid': True,
    'color': account_colors['light-grey'],
    'gridwidth': 0.5,
    'gridcolor': account_colors['dark-blue'],
    'linecolor': account_colors['light-grey'],
    'titlefont': {
        'size': 12,
        'color': account_colors['light-grey']},
    'tickfont': {
        'size': 11,
        'color': account_colors['light-grey']},
    'zeroline': False
}

account_font_family = 'Proxima Nova'

account_legend = {
    'orientation': 'h',
    'yanchor': 'bottom',
    'y': 1.01,
    'xanchor': 'right',
    'x': 1.05,
    'font': {'size': 9, 'color': account_colors['light-grey']}
}  # Legend will be on the top right, above the graph, horizontally

# Set top margin to in case there is a legend
account_margins = {'l': 5, 'r': 5, 't': 45, 'b': 15}

account_layout = Layout(
    font={'family': account_font_family},
    title=account_title,
    title_x=0.5,  # Align chart title to center
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=account_xaxis,
    yaxis=account_yaxis,
    height=270,
    legend=account_legend,
    margin=account_margins
)
