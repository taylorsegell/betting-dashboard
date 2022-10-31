from unicodedata import name
import plotly.express as px
import plotly.figure_factory as ff
from dash import dcc, html, dash_table, Input, Output
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import dash
from dash.dash_table.Format import Format, Group, Scheme
#import dash_table.FormatTemplate as FormatTemplate
from datetime import datetime as dt
from app import app

####################################################################################################
# 000 - FORMATTING INFO
####################################################################################################

# Corporate css formatting
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

quant_colors = [[0, '#445058'], [1, '#E44242']]

externalgraph_rowstyling = {
    'margin-left': '15px',
    'margin-right': '15px'
}

externalgraph_colstyling = {
    'border-radius': '10px',
    'border-style': 'solid',
    'border-width': '1px',
    'border-color': fanduel_colors['superdark-blue'],
    'background-color': fanduel_colors['superdark-blue'],
    'box-shadow': '0px 0px 17px 0px #CFD6DB',
    'padding-top': '10px'
}

filterdiv_borderstyling = {
    'border-radius': '0px 0px 10px 10px',
    'border-style': 'solid',
    'border-width': '1px',
    'border-color': fanduel_colors['light-blue'],
    'background-color': fanduel_colors['superdark-blue'],
    'box-shadow': '2px 5px 5px 1px #445058'
}

navbarcurrentpage = {
    'text-decoration': 'underline',
    'text-decoration-color': fanduel_colors['red'],
    'text-shadow': '0px 0px 1px #FFFFFF'
}

recapdiv = {
    'border-radius': '10px',
    'border-style': 'solid',
    'border-width': '1px',
    'border-color': '#F5F8FC',
    'margin-left': '15px',
    'margin-right': '15px',
    'margin-top': '15px',
    'margin-bottom': '15px',
    'padding-top': '5px',
    'padding-bottom': '5px',
    'background-color': '#1381E0'
}

recapdiv_text = {
    'text-align': 'left',
    'font-weight': '350',
    'color': fanduel_colors['white'],
    'font-size': '1.5rem',
    'letter-spacing': '0.04em'
}

# Corporate chart formatting

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

fanduel_layout = go.Layout(
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
fanduel_layout2 = go.Layout(
    font={'family': fanduel_font_family},
    title=fanduel_title,
    title_x=0.5,  # Align chart title to center
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=fanduel_xaxis,
    yaxis=fanduel_yaxis,
    legend=fanduel_legend,
    margin=fanduel_margins
)
####################################################################################################
# 000 - DATA MAPPING
####################################################################################################

####################################################################################################
# 000 - DATA MAPPING
####################################################################################################
df = pd.read_pickle('finalpickle.pkl')
new_df1 = df.copy()
new_df1.columns = new_df1.columns.str.replace(
    '[|_]', ' ', regex=True).str.title()
new_df1 = new_df1.rename(columns={'Wagerid': 'Wagers',
                                  'Playerid': 'Players', 'Rfm Score': 'RFM Score'})
groupdf = df.groupby(['placed_date', 'state', 'sport']).agg({'wagerid': 'count', 'playerid': pd.Series.nunique, 'decimal_odds': np.mean, 'gross_revenue': [
    np.mean, np.sum], 'rfm_score': np.mean, 'recency': np.mean, 'frequency': np.mean, 'rfm_segment': pd.Series.mode}).reset_index()
groupdf.sort_values(['placed_date', 'state', 'sport'], inplace=True)
groupdf.columns = groupdf.columns.map('|'.join).str.strip(
    '|').str.replace('[|_]', ' ', regex=True).str.title()
new_df = groupdf.rename(columns={'Wagerid Count': 'Wagers',
                        'Playerid Nunique': 'Players', 'Rfm Score Mean': 'RFM Score Mean'})


fields = {'Placed Date': 'Placed Date',
          'State': 'State',
          'Sport': 'Sport',
          'Wagers': 'Wagers',
          'Players': 'Players',
          'Decimal Odds Mean': 'Decimal Odds Mean',
          'Gross Revenue Mean': 'Gross Revenue Mean',
          'Gross Revenue Sum': 'Gross Revenue Sum',
          'RFM Score Mean': 'RFM Score Mean',
          'Recency Mean': 'Recency Mean',
          'Frequency Mean': 'Frequency Mean',
          'Status Mode': 'Status Mode'}

dformats = {
    fields['Placed Date']: '%d/%m/%Y'
}


# Format date field
new_df[fields['Placed Date']] = pd.to_datetime(
    new_df[fields['Placed Date']], format=dformats[fields['Placed Date']])


new_df['date_2'] = new_df[fields['Placed Date']].dt.date
min_dt = new_df['date_2'].min()
min_dt_str = str(min_dt)
max_dt = new_df['date_2'].max()
max_dt_str = str(max_dt)

# Initialise L1 dropdown options
both_ls = new_df['State'].unique()
state_all_2 = [
    {'label': k, 'value': k} for k in sorted(both_ls)
]
state_all_1 = [{'label': '(Select All)', 'value': 'All'}]
state_all = state_all_1 + state_all_2

# Initialise L2 dropdown options
sports = new_df['Sport'].unique()
sports_all_2 = [
    {'label': k, 'value': k} for k in sorted(sports)
]
sports_all_1 = [{'label': '(Select All)', 'value': 'All'}]
sports_all = sports_all_1 + sports_all_2
both_l2 = {}
for l1 in both_ls:
    l2 = new_df[new_df['State']
                == l1]['Sport'].unique()
    both_l2[l1] = l2


# SET UP END

####################################################################################################
# 000 - DEFINE ADDITIONAL FUNCTIONS
####################################################################################################


def group_wavg(df, gr_by_cols, weight, value):
    """This function returns a df grouped by the gr_by_cols and calculate the weighted avg based
    on the entries in the weight and value lists"""
    # Calculate weight * value columns
    wcols = []
    cols = []
    for i in range(0, len(value), 1):
        wcol = "w"+value[i]
        wcols.append(wcol)
        df[wcol] = df[weight[i]] * df[value[i]]
    # Group by summing the wcols and weight columns
    cols = weight
    for i in wcols:
        cols.append(i)
    df1 = df.groupby(gr_by_cols)[cols].agg('sum')
    df1.reset_index(inplace=True)
    # Divide wcols by weight and remove columns
    for i in range(0, len(value), 1):
        df1[value[i]] = df1[wcols[i]] / df1[weight[i]]
        df1.drop(wcols[i], axis='columns', inplace=True)

    return df1


def colorscale_generator(n, starting_col={'r': 20, 'g': 147, 'b': 255}, finish_col={'r': 68, 'g': 80, 'b': 88}):
    """This function generate a colorscale between two given rgb extremes, for an amount of data points
    The rgb should be specified as dictionaries"""
    r = starting_col['r']
    g = starting_col['g']
    b = starting_col['b']
    rf = finish_col['r']
    gf = finish_col['g']
    bf = finish_col['b']
    ri = (rf - r) / n
    gi = (gf - g) / n
    bi = (bf - b) / n
    color_i = 'rgb(' + str(r) + ',' + str(g) + ',' + str(b) + ')'
    my_colorscale = []
    my_colorscale.append(color_i)
    for i in range(n):
        r = r + ri
        g = g + gi
        b = b + bi
        color = 'rgb(' + str(round(r)) + ',' + \
            str(round(g)) + ',' + str(round(b)) + ')'
        my_colorscale.append(color)

    return my_colorscale


# Create a corporate colorcale
colors = colorscale_generator(n=11)

fanduel_colorscale = [
    [0.0, colors[0]],
    [0.1, colors[1]],
    [0.2, colors[2]],
    [0.3, colors[3]],
    [0.4, colors[4]],
    [0.5, colors[5]],
    [0.6, colors[6]],
    [0.7, colors[7]],
    [0.8, colors[8]],
    [0.9, colors[9]],
    [1.0, colors[10]]]

####################################################################################################
####################################################################################################
####################################################################################################
# Revenue PAGE
####################################################################################################
####################################################################################################
####################################################################################################


@app.callback(
    Output('reporting-groups-l2dropdown-revenue', 'options'),
    [Input('reporting-groups-l1dropdown-revenue', 'value')])
def l2dropdown_options(l1_dropdown_value):
    isselect_all = 'Start'  # Initialize isselect_all
    # Rembember that the dropdown value is a list !
    for i in l1_dropdown_value:
        if i == 'All':
            isselect_all = 'Y'
            break
        elif i != '':
            isselect_all = 'N'
        else:
            pass
    # Create options for individual selections
    if isselect_all == 'N':
        options_0 = []
        for i in l1_dropdown_value:
            options_0.append(both_l2[i])
        options_1 = []  # Extract string of string
        for i1 in options_0:
            for i2 in i1:
                options_1.append(i2)
        options_list = []  # Get unique values from the string
        for i in options_1:
            if i not in options_list:
                options_list.append(i)
            else:
                pass
        options_final_1 = [
            {'label': k, 'value': k} for k in sorted(options_list)]
        options_final_0 = [{'label': '(Select All)', 'value': 'All'}]
        options_final = options_final_0 + options_final_1
    # Create options for select all or none
    else:
        options_final_1 = [
            {'label': k, 'value': k} for k in sorted(sports)]
        options_final_0 = [{'label': '(Select All)', 'value': 'All'}]
        options_final = options_final_0 + options_final_1

    return options_final


####################################################################################################
# 000 - CALLBACK BABY
####################################################################################################


@app.callback(
    [Output('recap-table', 'data'), Output(
        'recap-table', 'columns')],  # , Output('recap-table', 'style_data_conditional')],
    [Input('date-picker-revenue', 'start_date'),
     Input('date-picker-revenue', 'end_date'),
     Input('reporting-groups-l1dropdown-revenue', 'value'),
     Input('reporting-groups-l2dropdown-revenue', 'value')])
def update_chart(start_date, end_date, reporting_l1_dropdown, reporting_l2_dropdown):
    start = dt.strptime(start_date, '%Y-%m-%d')
    end = dt.strptime(end_date, '%Y-%m-%d')

    # Filter based on the dropdowns
    isselect_all_l1 = 'Start'  # Initialize isselect_all
    isselect_all_l2 = 'Start'  # Initialize isselect_all
    # L1 selection (dropdown value is a list!)
    for i in reporting_l1_dropdown:
        if i == 'All':
            isselect_all_l1 = 'Y'
            break
        elif i != '':
            isselect_all_l1 = 'N'
        else:
            pass
    # Filter df according to selection
    if isselect_all_l1 == 'N':
        report_df_1 = new_df.loc[new_df['State'].isin(
            reporting_l1_dropdown), :].copy()
    else:
        report_df_1 = new_df.copy()
    # L2 selection (dropdown value is a list!)
    for i in reporting_l2_dropdown:
        if i == 'All':
            isselect_all_l2 = 'Y'
            break
        elif i != '':
            isselect_all_l2 = 'N'
        else:
            pass
    # Filter df according to selection
    if isselect_all_l2 == 'N':
        report_df = report_df_1.loc[report_df_1['Sport'].isin(
            reporting_l2_dropdown), :].copy()
    else:
        report_df = report_df_1.copy()
    del report_df_1

    # Filter based on the date filters
    df_1 = report_df.loc[(report_df['Placed Date'] >= start) & (
        report_df['Placed Date'] <= end), :].copy()
    del report_df

    # Aggregate df
    def readable(num, prefix=''):
        for unit in ['', ' Mil', ' Bil', ' Tril']:
            if abs(num) < 1000000.0:
                return f"{prefix}{num:.2f}{unit}"
            num /= 1000000.0
        return f"{prefix}{num:.1f}Yi"

    df_1 = new_df1
    METRIC = ['Total']
    GGR = [readable(df_1['Gross Revenue'].sum(), '$')]
    RFM = [readable(df_1['RFM Score'].mean(), '')]
    NULL = ['']
    PLAYERS = [readable(df_1['Players'].nunique(), '')]
    WAGERS = [readable(df_1['Wagers'].nunique(), '')]
    df = pd.DataFrame({  # 'Total': METRIC,
        'GGR': GGR,
        'Players': PLAYERS,
        'Wagers': WAGERS,
        'RFM Score': RFM})

    # Configure table data
    data = df.to_dict('records')
    columns = [
        #{'id': 'Total', 'name': 'Total'},
        {'id': 'GGR', 'name': 'GGR', 'type': 'text'},
        {'id': 'Players', 'name': 'Players',  'type': 'text'},
        {'id': 'Wagers', 'name': 'Wagers', 'type': 'text'},
        #{'id': '|', 'name': '      '},
        {'id': 'RFM Score', 'name': 'RFM Mean', 'type': 'text'},
    ]

    # Configure conditional formatting
    conditional_style = [
        {  # 'if': {
            #  'filter_query': '{Result} >= {Target} && {Target} > 0',
            # 'column_id': 'Target_Percent'},
            'backgroundColor': fanduel_colors['light-blue'],
            'color': fanduel_colors['dark-blue'],
            'fontWeight': 'bold'
        },
        ''' {  # 'if': {
            #  'filter_query': '{Result} < {Target} && {Target} > 0',
            # 'column_id': 'Target_Percent'},
            'backgroundColor': fanduel_colors['red'],
            'color': fanduel_colors['dark-blue'],
            'fontWeight': 'bold'
        },'''
    ]

    return data, columns  # , conditional_style

####################################################################################################
# 003 - REVENUE COUNT DAY
####################################################################################################


@app.callback(
    Output('revenue-count-day', 'figure'),
    [Input('date-picker-revenue', 'start_date'),
     Input('date-picker-revenue', 'end_date'),
     Input('reporting-groups-l1dropdown-revenue', 'value'),
     Input('reporting-groups-l2dropdown-revenue', 'value')])
def update_chart(start_date, end_date, reporting_l1_dropdown, reporting_l2_dropdown):
    start = dt.strptime(start_date, '%Y-%m-%d')
    end = dt.strptime(end_date, '%Y-%m-%d')

    # Filter based on the dropdowns
    isselect_all_l1 = 'Start'  # Initialize isselect_all
    isselect_all_l2 = 'Start'  # Initialize isselect_all
    # L1 selection (dropdown value is a list!)
    for i in reporting_l1_dropdown:
        if i == 'All':
            isselect_all_l1 = 'Y'
            break
        elif i != '':
            isselect_all_l1 = 'N'
        else:
            pass
    # Filter df according to selection
    if isselect_all_l1 == 'N':
        report_df_1 = new_df.loc[new_df['State'].isin(
            reporting_l1_dropdown), :].copy()
    else:
        report_df_1 = new_df.copy()
    # L2 selection (dropdown value is a list!)
    for i in reporting_l2_dropdown:
        if i == 'All':
            isselect_all_l2 = 'Y'
            break
        elif i != '':
            isselect_all_l2 = 'N'
        else:
            pass
    # Filter df according to selection
    if isselect_all_l2 == 'N':
        report_df = report_df_1.loc[report_df_1['Sport'].isin(
            reporting_l2_dropdown), :].copy()
    else:
        report_df = report_df_1.copy()
    del report_df_1

    # Aggregate df
    val_cols = ['Gross Revenue Sum', 'Recency Mean']
    report_df = report_df.groupby('Placed Date')[val_cols].agg('sum')
    report_df.reset_index(inplace=True)

    # Filter based on the date filters
    df = report_df.loc[(report_df['Placed Date'] >= start) & (
        report_df['Placed Date'] <= end), :].copy()
    del report_df

    # Build graph
    hovertemplate_xy = (
        "<i>Day</i>: %{x|%a, %d-%b-%Y}<br>" +
        "<i>Revenue</i>: %{y:,d}" +
        "<extra></extra>")  # Remove trace info
    data = go.Scatter(
        x=df['Placed Date'],
        y=df['Gross Revenue Sum'],
        line={'color': fanduel_colors['red'], 'width': 0.5},
        hovertemplate=hovertemplate_xy)
    fig = go.Figure(data=data, layout=fanduel_layout)
    ''' fig.add_trace(
                go.Bar(
                    x=df['Placed Date'],
                    y=df['Gross Revenue Sum'],
                    marker={'color': fanduel_colors['light-blue'],
                    'opacity': 0.75}))'''
    # hovertemplate=hovertemplate_xy

    fig.update_layout(
        title={'text': "Revenue per Day"},
        xaxis={
            'title': "Day",
            'tickformat': "%d-%m-%y"},
        yaxis={
            'title': "Revenue (units)"},
        showlegend=False)

    return fig

####################################################################################################
# 004 - REVENUE COUNT MONTH
####################################################################################################


@app.callback(
    Output('revenue-count-month', 'figure'),
    [Input('date-picker-revenue', 'start_date'),
     Input('date-picker-revenue', 'end_date'),
     Input('reporting-groups-l1dropdown-revenue', 'value'),
     Input('reporting-groups-l2dropdown-revenue', 'value')])
def update_chart(start_date, end_date, reporting_l1_dropdown, reporting_l2_dropdown):
    start = dt.strptime(start_date, '%Y-%m-%d')
    end = dt.strptime(end_date, '%Y-%m-%d')

    # Filter based on the dropdowns
    isselect_all_l1 = 'Start'  # Initialize isselect_all
    isselect_all_l2 = 'Start'  # Initialize isselect_all
    # L1 selection (dropdown value is a list!)
    for i in reporting_l1_dropdown:
        if i == 'All':
            isselect_all_l1 = 'Y'
            break
        elif i != '':
            isselect_all_l1 = 'N'
        else:
            pass
    # Filter df according to selection
    if isselect_all_l1 == 'N':
        report_df_1 = new_df.loc[new_df['State'].isin(
            reporting_l1_dropdown), :].copy()
    else:
        report_df_1 = new_df.copy()
    # L2 selection (dropdown value is a list!)
    for i in reporting_l2_dropdown:
        if i == 'All':
            isselect_all_l2 = 'Y'
            break
        elif i != '':
            isselect_all_l2 = 'N'
        else:
            pass
    # Filter df according to selection
    if isselect_all_l2 == 'N':
        report_df = report_df_1.loc[report_df_1['Sport'].isin(
            reporting_l2_dropdown), :].copy()
    else:
        report_df = report_df_1.copy()
    del report_df_1

    # Filter based on the date filters
    df1 = report_df.loc[(report_df['Placed Date'] >= start) & (
        report_df['Placed Date'] <= end), :].copy()
    df1['month'] = df1['Placed Date'].dt.month
    del report_df

    # Aggregate df
    val_cols = ['Gross Revenue Sum', 'Players']
    df = df1.groupby('month')[val_cols].agg('sum')
    df.reset_index(inplace=True)
    del df1

    # Build graph
    hovertemplate_xy = (
        "<i>Month</i>: %{x}<br>" +
        "<i>Revenue</i>: %{y:,d}" +
        "<extra></extra>")  # Remove trace info
    data = go.Bar(
        x=df['month'],
        y=df['Gross Revenue Sum'],
        marker={'color': df['Gross Revenue Sum'],
                'colorscale': [fanduel_colors['dark-blue'], fanduel_colors['dark-blue'],
                               fanduel_colors['light-blue'], fanduel_colors['red'], fanduel_colors['red']], 'opacity': 0.75},
        hovertemplate=hovertemplate_xy)
    fig = go.Figure(data=data, layout=fanduel_layout)

    # Add target% as line on secondary axis
    ''' hovertemplate_xy2 = (
            "<i>Month</i>: %{x}<br>" +
            "<i>Target percentage</i>: %{y:%}" +
            "<extra></extra>")'''  # Remove trace info

    fig.update_layout(
        title={'text': "Revenue per Month"},
        xaxis={
            'title': "Month",
            # Display x values with different labels
            'tickvals': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            'ticktext': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']},
        yaxis={'title': "Revenue (units)"},
        showlegend=False)
    fig.update_layout(yaxis2=fanduel_yaxis)
    fig.update_layout(
        yaxis2={
            'title': "% over Revenue Frequency",
            'side': "right",
            'showgrid': False,
            'tickformat': ".0%",
            'range': [0, 1.15],
            'overlaying': "y",
            'linewidth': 1},
        hovermode='x')

    return fig

####################################################################################################
# 005 - WEEKLY-WEEKDAY REVENUE HEATMAP
####################################################################################################


@app.callback(
    Output('revenue-weekly-heatmap', 'figure'),
    [Input('date-picker-revenue', 'start_date'),
     Input('date-picker-revenue', 'end_date'),
     Input('reporting-groups-l1dropdown-revenue', 'value'),
     Input('reporting-groups-l2dropdown-revenue', 'value')])
def update_chart(start_date, end_date, reporting_l1_dropdown, reporting_l2_dropdown):
    start = dt.strptime(start_date, '%Y-%m-%d')
    end = dt.strptime(end_date, '%Y-%m-%d')

    # Filter based on the dropdowns
    isselect_all_l1 = 'Start'  # Initialize isselect_all
    isselect_all_l2 = 'Start'  # Initialize isselect_all
    # L1 selection (dropdown value is a list!)
    for i in reporting_l1_dropdown:
        if i == 'All':
            isselect_all_l1 = 'Y'
            break
        elif i != '':
            isselect_all_l1 = 'N'
        else:
            pass
    # Filter df according to selection
    if isselect_all_l1 == 'N':
        report_df_1 = new_df.loc[new_df['State'].isin(
            reporting_l1_dropdown), :].copy()
    else:
        report_df_1 = new_df.copy()
    # L2 selection (dropdown value is a list!)
    for i in reporting_l2_dropdown:
        if i == 'All':
            isselect_all_l2 = 'Y'
            break
        elif i != '':
            isselect_all_l2 = 'N'
        else:
            pass
    # Filter df according to selection
    if isselect_all_l2 == 'N':
        report_df = report_df_1.loc[report_df_1['Sport'].isin(
            reporting_l2_dropdown), :].copy()
    else:
        report_df = report_df_1.copy()
    del report_df_1

    # Filter based on the date filters
    df1 = report_df.loc[(report_df['Placed Date'] >= start) & (
        report_df['Placed Date'] <= end), :].copy()
    df1['week'] = df1['Placed Date'].dt.strftime("%V")
    df1['weekday'] = df1['Placed Date'].dt.weekday
    del report_df

    # Aggregate df
    val_cols = ['Gross Revenue Sum']
    df = df1.groupby(['week', 'weekday'])[val_cols].agg('sum')
    df.reset_index(inplace=True)
    del df1

    # Build graph
    hovertemplate_here = (
        "<i>Weekday</i>: %{x}<br>" +
        "<i>Week</i>: %{y}<br>" +
        "<i>Revenue</i>: $ %{z}" +
        "<extra></extra>")  # Remove trace info
    data = go.Heatmap(
        x=df['weekday'],
        y=df['week'],
        z=df['Gross Revenue Sum'].round(2),
        hovertemplate=hovertemplate_here,
        hoverongaps=False,
        colorscale=[fanduel_colors['dark-blue'], fanduel_colors['dark-blue'],
                    fanduel_colors['light-blue'], fanduel_colors['red'], fanduel_colors['red']],
        showscale=False,
        xgap=1,
        ygap=1)
    fig = go.Figure(data=data, layout=fanduel_layout)
    fig.update_layout(
        title={'text': "Heatmap: Revenue by Week and Weekeday"},
        xaxis={
            'title': "Weekday",
            # Display x values with different labels
            'tickvals': [0, 1, 2, 3, 4, 5, 6],
            'ticktext': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']},
        yaxis={
            'title': "Calendar Week",
            'showgrid': False})

    return fig

####################################################################################################
# 006 - REVENUE BY state
####################################################################################################


@app.callback(
    Output('revenue-count-state', 'figure'),
    [Input('date-picker-revenue', 'start_date'),
     Input('date-picker-revenue', 'end_date'),
     Input('reporting-groups-l1dropdown-revenue', 'value'),
     Input('reporting-groups-l2dropdown-revenue', 'value')])
def update_chart(start_date, end_date, reporting_l1_dropdown, reporting_l2_dropdown):
    start = dt.strptime(start_date, '%Y-%m-%d')
    end = dt.strptime(end_date, '%Y-%m-%d')

    # Filter based on the dropdowns
    isselect_all_l1 = 'Start'  # Initialize isselect_all
    isselect_all_l2 = 'Start'  # Initialize isselect_all
    # L1 selection (dropdown value is a list!)
    for i in reporting_l1_dropdown:
        if i == 'All':
            isselect_all_l1 = 'Y'
            break
        elif i != '':
            isselect_all_l1 = 'N'
        else:
            pass
    # Filter df according to selection
    if isselect_all_l1 == 'N':
        report_df_1 = new_df.loc[new_df['State'].isin(
            reporting_l1_dropdown), :].copy()
    else:
        report_df_1 = new_df.copy()
    # L2 selection (dropdown value is a list!)
    for i in reporting_l2_dropdown:
        if i == 'All':
            isselect_all_l2 = 'Y'
            break
        elif i != '':
            isselect_all_l2 = 'N'
        else:
            pass
    # Filter df according to selection
    if isselect_all_l2 == 'N':
        report_df = report_df_1.loc[report_df_1['Sport'].isin(
            reporting_l2_dropdown), :].copy()
    else:
        report_df = report_df_1.copy()
    del report_df_1

    # Filter based on the date filters
    df1 = report_df.loc[(report_df['Placed Date'] >= start) & (
        report_df['Placed Date'] <= end), :].copy()
    del report_df

    # Aggregate df
    val_cols = ['Gross Revenue Sum']
    df = df1.groupby('State')[val_cols].agg('sum')
    df.reset_index(inplace=True)
    df.sort_values('State', axis=0,
                   ascending=True, inplace=True, na_position='last')
    del df1

    # Prepare incr % data
    hover_text = []
    sale_perc = []
    sale_base = [0]
    sale_b = 0
    revenue_tot = df['Gross Revenue Sum'].sum()
    for index, row in df.iterrows():
        sale_p = row['Gross Revenue Sum']/revenue_tot
        hover_text.append(("<i>State</i>: {}<br>" +
                           "<i>Revenue</i>: {:.2%}" +
                           "<extra></extra>").format(row['State'],
                                                     sale_p))
        sale_b = sale_b + sale_p
        sale_perc.append(sale_p)
        sale_base.append(sale_b)
    sale_base = sale_base[:-1]
    df['sale_p'] = sale_perc
    df['hovertext'] = hover_text

    # Build graph
    data = go.Bar(
        x=df['State'],
        y=df['sale_p'],
        base=sale_base,
        marker={'color': [fanduel_colors['dark-blue'], fanduel_colors['light-blue'], fanduel_colors['red']],
                'opacity': 0.75},
        hovertemplate=df['hovertext'])
    fig = go.Figure(data=data, layout=fanduel_layout)
    fig.update_layout(
        title={'text': "Revenue Percentage by State"},
        xaxis={'title': "State", 'tickangle': 0},
        yaxis={
            'title': "Revenue Percentage",
            'tickformat': ".0%",
            'range': [0, 1]},
        barmode='group',
        showlegend=False)

    return fig

####################################################################################################
# 007 - REVENUE BUBBLE CHART
####################################################################################################


@app.callback(
    Output('revenue-bubble-county', 'figure'),
    [Input('date-picker-revenue', 'start_date'),
     Input('date-picker-revenue', 'end_date'),
     Input('reporting-groups-l1dropdown-revenue', 'value'),
     Input('reporting-groups-l2dropdown-revenue', 'value')])
def update_chart(start_date, end_date, reporting_l1_dropdown, reporting_l2_dropdown):
    start = dt.strptime(start_date, '%Y-%m-%d')
    end = dt.strptime(end_date, '%Y-%m-%d')

    # Filter based on the dropdowns
    isselect_all_l1 = 'Start'  # Initialize isselect_all
    isselect_all_l2 = 'Start'  # Initialize isselect_all
    # L1 selection (dropdown value is a list!)
    for i in reporting_l1_dropdown:
        if i == 'All':
            isselect_all_l1 = 'Y'
            break
        elif i != '':
            isselect_all_l1 = 'N'
        else:
            pass
    # Filter df according to selection
    if isselect_all_l1 == 'N':
        report_df_1 = new_df.loc[new_df['State'].isin(
            reporting_l1_dropdown), :].copy()
    else:
        report_df_1 = new_df.copy()
    # L2 selection (dropdown value is a list!)
    for i in reporting_l2_dropdown:
        if i == 'All':
            isselect_all_l2 = 'Y'
            break
        elif i != '':
            isselect_all_l2 = 'N'
        else:
            pass
    # Filter df according to selection
    if isselect_all_l2 == 'N':
        report_df = report_df_1.loc[report_df_1['Sport'].isin(
            reporting_l2_dropdown), :].copy()
    else:
        report_df = report_df_1.copy()
    del report_df_1

    # Filter based on the date filters
    df1 = report_df.loc[(report_df['Placed Date'] >= start) & (
        report_df['Placed Date'] <= end), :].copy()
    del report_df

    # Aggregate df
    val_cols = ['Gross Revenue Sum',
                'Players', 'RFM Score Mean']
    df = df1.groupby('State')[val_cols].agg(
        {'Gross Revenue Sum': 'sum', 'Players': 'count', 'RFM Score Mean': 'mean'})
    df.reset_index(inplace=True)
    df['rev_per_cl'] = df['Gross Revenue Sum']
    del df1

    # Build graph
    # Add hover text info on the df
    hover_text = []
    for index, row in df.iterrows():
        hover_text.append(('<i>State</i>: {}<br>' +
                          '<i>Revenue</i>: ${:,.2f}<br>' +
                           '<i>Players</i>: {:,.0f}<br>' +
                           '<i>RFM Mean</i>: {:,.2f}' +
                           '<extra></extra>').format(row['State'],
                                                     row['Gross Revenue Sum'],
                                                     row['Players'],
                                                     row['RFM Score Mean']))
    df['hovertext'] = hover_text
    sizeref = 2.*max(df['Gross Revenue Sum'])/(100**2)
    df['position'] = [1, 2, 3]
    # Create bubbles (1 color per state, one trace per sport)
    state_names = sorted(df['State'].unique())
    countries = len(state_names)
    colorscale = colorscale_generator(n=countries, starting_col={
                                      'r': 57, 'g': 81, 'b': 85}, finish_col={'r': 251, 'g': 251, 'b': 252})

    fig = go.Figure(layout=fanduel_layout)
    i = 0
    for co in state_names:
        color = [fanduel_colors['dark-blue'], fanduel_colors['dark-blue'], fanduel_colors['light-blue'],
                 fanduel_colors['red'], fanduel_colors['red']]
        i = i+1
        df_i = df.loc[df['State'] == co, :].copy()
        fig.add_trace(
            go.Scatter(
                x=df_i['position'],
                y=df_i['rev_per_cl'],
                name=co,
                hovertemplate=df_i['hovertext'],
                marker_size=df_i['Gross Revenue Sum'],
                marker={
                    'color': color[i],
                    'line_width': 1,
                    'line': {'color': fanduel_colors['light-grey']}
                })
        )

    fig.update_traces(mode='markers', marker={
                      'sizemode': 'area', 'sizeref': sizeref})
    fanduel_margins_here = fanduel_margins
    fanduel_margins_here['t'] = 65
    fig.update_layout(
        title={'text': "Revenue Total by State"},
        xaxis={'title': "State", 'tickangle': 0},
        yaxis={'title': "Revenue (GGR)"},
        margin=fanduel_margins_here)
    fig.update_xaxes(showticklabels=False)

    return fig

####################################################################################################
# 008 - REVENUE BY state & CITY
####################################################################################################


@app.callback(
    Output('revenue-count-sport', 'figure'),
    [Input('date-picker-revenue', 'start_date'),
     Input('date-picker-revenue', 'end_date'),
     Input('reporting-groups-l1dropdown-revenue', 'value'),
     Input('reporting-groups-l2dropdown-revenue', 'value')])
def update_chart(start_date, end_date, reporting_l1_dropdown, reporting_l2_dropdown):
    start = dt.strptime(start_date, '%Y-%m-%d')
    end = dt.strptime(end_date, '%Y-%m-%d')

    # Filter based on the dropdowns
    isselect_all_l1 = 'Start'  # Initialize isselect_all
    isselect_all_l2 = 'Start'  # Initialize isselect_all
    # L1 selection (dropdown value is a list!)
    for i in reporting_l1_dropdown:
        if i == 'All':
            isselect_all_l1 = 'Y'
            break
        elif i != '':
            isselect_all_l1 = 'N'
        else:
            pass
    # Filter df according to selection
    if isselect_all_l1 == 'N':
        report_df_1 = new_df.loc[new_df['State'].isin(
            reporting_l1_dropdown), :].copy()
    else:
        report_df_1 = new_df.copy()
    # L2 selection (dropdown value is a list!)
    for i in reporting_l2_dropdown:
        if i == 'All':
            isselect_all_l2 = 'Y'
            break
        elif i != '':
            isselect_all_l2 = 'N'
        else:
            pass
    # Filter df according to selection
    if isselect_all_l2 == 'N':
        report_df = report_df_1.loc[report_df_1['Sport'].isin(
            reporting_l2_dropdown), :].copy()
    else:
        report_df = report_df_1.copy()
    del report_df_1

    # Filter based on the date filters
    df1 = report_df.loc[(report_df['Placed Date'] >= start) & (
        report_df['Placed Date'] <= end), :].copy()
    del report_df

    # Aggregate df
    val_cols = {'Gross Revenue Sum': np.sum, 'Recency Mean': np.mean}
    df = df1.groupby(['State',
                      'Sport']).agg(val_cols)
    df.reset_index(inplace=True)
    # Include hover data
    hover_text = []
    for index, row in df.iterrows():
        hover_text.append(("<i>State</i>: {}<br>" +
                           "<i>Sport</i>: {}<br>" +
                           "<i>Revenue</i>: ${:,.2f}<br>" +
                           "<i>Recency Avg.</i>: {:,.2f}" +
                           "<extra></extra>").format(row['State'],
                                                     row['Sport'],
                                                     row['Gross Revenue Sum'],
                                                     row['Recency Mean']))
    df['hovertext'] = hover_text
    df['l1l2'] = df['State'] + \
        "_" + df['Sport']
    # Generate colors
    ncolors = len(df['Sport'].unique())
    colorscale = colorscale_generator(n=ncolors)

    clist3 = ['#0E4AC7', '#86a4e3', '#1381E0', '#c29898', '#818E95',
              '#BF2D2D', '#40454b']  # '#E24048', '#7fafda']
    # Build graph
    data = []
    i = 0
    for l in sorted(df['l1l2']):
        df_l = df.loc[(df['l1l2'] == l), :].copy()
        trace = go.Bar(
            name=l,
            x=df_l['State'],
            y=df_l['Gross Revenue Sum'],
            hovertemplate=df_l['hovertext'],
            marker={
                'color': (clist3*3)[i],
                'opacity': 0.85,
                'line_width': 1,
                'line': {'color': colorscale}
            }
        )
        i = i+1
        data.append(trace)
    fig = go.Figure(data=data, layout=fanduel_layout)
    fig.update_layout(
        barmode='relative',
        title={'text': "Revenue by State & Sport"},
        xaxis={'title': "State", 'tickangle': 0},
        yaxis={'title': "Revenue (GGR)"},
        showlegend=False)

    return fig


####################################################################################################
# 009 - PAGE 2
####################################################################################################
sport_period_df = pd.read_pickle('sports-period.pkl')
neg_color = '#E44242'
pos_color = '#1381E0'
df['dayname'] = df.placed_date.dt.day_name()
df['monthname'] = df.placed_date.dt.month_name()
sport_period = df[['monthname', 'dayname', 'gross_revenue', 'sport',
                   'placed_day_month', 'decimal_odds', 'gross_revenue_margin', 'bet_type']]
mnths = list(sport_period.monthname.unique())


@app.callback(
    Output("rev-graph", "figure"),
    Input("period", "value"),
    Input("sports", "value"))
def generate_chart(p, s):
    parlay = sport_period[sport_period['bet_type'] == 'parlay']
    straight = sport_period[sport_period['bet_type'] == 'straight']
    tmp2 = parlay.groupby([p, 'sport', 'bet_type']).agg(
        {"gross_revenue": "sum", 'decimal_odds': 'mean'}).reset_index()
    tmp3 = straight.groupby([p, 'sport', 'bet_type']).agg(
        {"gross_revenue": "sum", 'decimal_odds': 'mean'}).reset_index()
    sp = list(tmp3.sport.unique())
    sp.append('All')
    #xaxisorder = {'categoryorder': 'array', 'categoryarray': mnths}
    #tmp3["color"] = np.where(tmp3["gross_revenue"] < 0, neg_color, pos_color)
    if s == 'All':
        fig = go.Figure()
        fig.add_trace(go.Bar(x=tmp3[p],
                             y=tmp3.gross_revenue,
                             # marker_color=tmp3['color'],
                             hovertext=tmp3.sport,
                             name='Straight'))
        fig.add_trace(go.Bar(x=tmp2[p],
                             y=tmp2.gross_revenue,
                             # marker_color=tmp3['color'],
                             hovertext=tmp2.sport,
                             name='Parlay'))

        # , xaxis={'categoryorder':'array', 'categoryarray':sp})
        fig.update_layout(barmode='group', title='<b>All Sports</b>')
        fig.update_yaxes(
            title_text="<b>Total Revenue</b>")
        fig.update_layout(fanduel_layout2)
    else:
        masks = tmp3[tmp3['sport'] == s]
        maskp = tmp2[tmp2['sport'] == s]
        fig = go.Figure()
        fig.add_trace(go.Bar(x=masks[p],
                             y=masks.gross_revenue,
                             # marker_color=mask['color'],
                             name="Straight",
                             text=masks['bet_type']
                             ))
        fig.add_trace(go.Bar(x=maskp[p],
                             y=maskp.gross_revenue,
                             # marker_color=mask['color'],
                             name="Parlay",
                             text=maskp['bet_type']))

        fig.update_layout(barmode='group',
                          title='Revenue From the <b>'+s+'</b>')
        fig.update_xaxes(categoryorder='array', categoryarray=mnths)
        fig.update_yaxes(title_text="<b>Total Revenue</b>")

        fig.update_layout(fanduel_layout2)
    return fig


####################################################################################################
# 009 - PAGE 3
####################################################################################################
# pd.reset_option("display.float_format")
######################## Graph 1 #####################
cohort_data = pd.read_csv(
    'retention_data.csv')
cohort_counts = cohort_data.pivot(
    index='Month Year', columns='Cohort Index', values='Playerid')
cohort_size = cohort_counts.iloc[:, 0]
retention = cohort_counts.divide(cohort_size, axis=0)
retention.index = pd.to_datetime(retention.index).strftime("%B %Y")
cohort_counts.index = pd.to_datetime(cohort_counts.index).strftime("%B %Y")


def make_heatmap(tri_df, title):
    df_mask = tri_df
    z = df_mask.to_numpy()
    z_text = np.around(z, 2)

    fig = ff.create_annotated_heatmap(z=z_text,
                                      x=df_mask.columns.tolist(),
                                      y=df_mask.columns.tolist(),
                                      colorscale=[
                                          fanduel_colors['dark-blue'], fanduel_colors['light-blue'], fanduel_colors['red']],
                                      showscale=True, ygap=1, xgap=1
                                      )

    fig.update_xaxes(side="bottom")
    fig.update_annotations(visible=False)
    fig.update_layout(
        title_x=0.5,
        height=700,
        yaxis_title='Cohort Month',
        xaxis_title='Months Since',
        xaxis_showgrid=False,
        yaxis_showgrid=False,
        xaxis_zeroline=False,
        yaxis_zeroline=False,
        yaxis=dict(
            tickmode='array',
            tickvals=list(range(1, 14)),
            ticktext=list(tri_df.index)
        ),
        yaxis_autorange='reversed',
        template='plotly_white'
    )

    # NaN values are not handled automatically and are displayed in the figure
    # So we need to get rid of the text manually
    for i in range(len(fig.layout.annotations)):
        if fig.layout.annotations[i].text == 'nan':
            fig.layout.annotations[i].text = ""
    for i in range(len(fig.layout.annotations)):
        fig.layout.annotations[i].font.size = 12
    '''fig.update_traces(hovertemplate='Average '+title+':%{z:.2%}<br>Month: %{y} <br>Cohort: %{y}')
    fig'''
    return fig


@app.callback(
    Output("retention-graph", "figure"),
    [Input("cohorts", "value")]
)
def update_tri(m):
    if m == 'cohort_size':
        fig = make_heatmap(cohort_counts, 'Cohorts Size')
        fig.update_traces(
            hovertemplate='Total Players: %{z:0}<br>Cohort Month: %{y} <br>Months Since: %{x}')
        fig.update_layout(fanduel_layout2)
        fig.update_layout(font=dict(color='white'))
    else:
        # m == 'cohort_retention':
        fig = make_heatmap(retention, 'Retention')
        fig.update_traces(
            hovertemplate='Average Retention: %{z:.2%}<br>Cohort Month: %{y} <br>Months Since: %{y}')
        fig.update_layout(fanduel_layout2)
        fig.update_layout(font=dict(color='white'))

    return fig


rfd = df.groupby(['playerid', 'state', 'sport', 'rf_segment']).agg({'recency': 'mean', 'frequency': 'mean',
                                                                    'monetaryvalue': 'sum'}).round(1).reset_index()
rfd = rfd.groupby(['state', 'sport', 'rf_segment']).agg({'recency': 'mean', 'frequency': ['mean', 'sum'],
                                                         'monetaryvalue': ['mean', 'sum', 'count']}).round(1).sort_values(('monetaryvalue', 'count')).reset_index()


def unmulti_cols(df):
    df.columns = df.columns.map('_'.join).str.strip('_')
    return df.columns
    unmulti_cols(rf)


unmulti_cols(rfd)
rfd.columns = rfd.columns.str.replace(
    'monetaryvalue_count', 'count').str.replace('monetaryvalue_', 'money_spent_')
rfd.rf_segment = rfd.rf_segment.str.replace('_', ' ').str.title()
rfd.columns = rfd.columns.str.replace('_', ' ').str.title()


def update_treemap(col):
    fig = px.treemap(rfd, path=[px.Constant("Sportsbook"), 'Rf Segment', col], values='Count', color='Money Spent Mean',
                     color_continuous_scale=[fanduel_colors['dark-blue'], fanduel_colors['dark-blue'],
                                             fanduel_colors['light-blue'], fanduel_colors['red'], fanduel_colors['red']],
                     color_continuous_midpoint=np.average(rfd['Money Spent Mean'], weights=rfd['Count']))
    return fig


@app.callback(
    Output("treemap_rfm", "figure"),
    [Input("col1", "value")])
def update_tree(n):
    if n == 'sports':
        x = 'Sport'
        fig = update_treemap(x)
        fig.update_traces(
            hovertemplate='Average Retention: %{label}<br>Cohort Month: %{value} <br>Months Since: %{parent}', marker_line_color='black')
        fig.update_layout(fanduel_layout2)
        fig.update_layout(font=dict(color='white'),
                          height=700)
    elif n == 'states':
        x = 'State'
        fig = update_treemap(x)
        fig.update_traces(
            hovertemplate='Average Retention: %{label}<br>Cohort Month: %{value} <br>Months Since: %{parent}', marker_line_color='black')
        fig.update_layout(fanduel_layout2)
        fig.update_layout(font=dict(color='white'),
                          height=700)
    return fig
