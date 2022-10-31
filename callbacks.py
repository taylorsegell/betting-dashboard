from dash import dcc, html, dash_table
import plotly.graph_objs as go
import pandas as pd
import numpy as np
import dash
from dash_table.Format import Format, Group, Scheme
import dash_table.FormatTemplate as FormatTemplate
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

####################################################################################################
# 000 - DATA MAPPING
####################################################################################################

# Revenue mapping
revenue_filepath = 'data/datasource.xlsx'

revenue_fields = {
    'date': 'Date',
    'reporting_group_l1': 'Country',
    'reporting_group_l2': 'City',
    'revenue': 'Revenue Units',
    'revenues': 'Revenues',
    'revenue target': 'Revenue Targets',
    'rev target': 'Rev Targets',
    'num clients': 'nClients'
}
revenue_formats = {
    revenue_fields['date']: '%d/%m/%Y'
}

####################################################################################################
# 000 - IMPORT DATA
####################################################################################################

###########################
# Import revenue data
xls = pd.ExcelFile(revenue_filepath)
revenue_import = xls.parse('Static')

# Format date field
revenue_import[revenue_fields['date']] = pd.to_datetime(
    revenue_import[revenue_fields['date']], format=revenue_formats[revenue_fields['date']])
revenue_import['date_2'] = revenue_import[revenue_fields['date']].dt.date
min_dt = revenue_import['date_2'].min()
min_dt_str = str(min_dt)
max_dt = revenue_import['date_2'].max()
max_dt_str = str(max_dt)

# Create L1 dropdown options
repo_groups_l1 = revenue_import[revenue_fields['reporting_group_l1']].unique()
repo_groups_l1_all_2 = [
    {'label': k, 'value': k} for k in sorted(repo_groups_l1)
]
repo_groups_l1_all_1 = [{'label': '(Select All)', 'value': 'All'}]
repo_groups_l1_all = repo_groups_l1_all_1 + repo_groups_l1_all_2

# Initialise L2 dropdown options
repo_groups_l2 = revenue_import[revenue_fields['reporting_group_l2']].unique()
repo_groups_l2_all_2 = [
    {'label': k, 'value': k} for k in sorted(repo_groups_l2)
]
repo_groups_l2_all_1 = [{'label': '(Select All)', 'value': 'All'}]
repo_groups_l2_all = repo_groups_l2_all_1 + repo_groups_l2_all_2
repo_groups_l1_l2 = {}
for l1 in repo_groups_l1:
    l2 = revenue_import[revenue_import[revenue_fields['reporting_group_l1']]
                        == l1][revenue_fields['reporting_group_l2']].unique()
    repo_groups_l1_l2[l1] = l2

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
# REVENUE PAGE
####################################################################################################
####################################################################################################
####################################################################################################

####################################################################################################
# 001 - L2 DYNAMIC DROPDOWN OPTIONS
####################################################################################################


@app.callback(
    dash.dependencies.Output('reporting-groups-l2dropdown-revenue', 'options'),
    [dash.dependencies.Input('reporting-groups-l1dropdown-revenue', 'value')])
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
            options_0.append(repo_groups_l1_l2[i])
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
            {'label': k, 'value': k} for k in sorted(repo_groups_l2)]
        options_final_0 = [{'label': '(Select All)', 'value': 'All'}]
        options_final = options_final_0 + options_final_1

    return options_final

####################################################################################################
# 002 - RECAP TABLE
####################################################################################################


@app.callback(
    [dash.dependencies.Output('recap-table', 'data'), dash.dependencies.Output(
        'recap-table', 'columns'), dash.dependencies.Output('recap-table', 'style_data_conditional')],
    [dash.dependencies.Input('date-picker-revenue', 'start_date'),
     dash.dependencies.Input('date-picker-revenue', 'end_date'),
     dash.dependencies.Input('reporting-groups-l1dropdown-revenue', 'value'),
     dash.dependencies.Input('reporting-groups-l2dropdown-revenue', 'value')])
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
        revenue_df_1 = revenue_import.loc[revenue_import[revenue_fields['reporting_group_l1']].isin(
            reporting_l1_dropdown), :].copy()
    else:
        revenue_df_1 = revenue_import.copy()
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
        revenue_df = revenue_df_1.loc[revenue_df_1[revenue_fields['reporting_group_l2']].isin(
            reporting_l2_dropdown), :].copy()
    else:
        revenue_df = revenue_df_1.copy()
    del revenue_df_1

    # Filter based on the date filters
    df_1 = revenue_df.loc[(revenue_df[revenue_fields['date']] >= start) & (
        revenue_df[revenue_fields['date']] <= end), :].copy()
    del revenue_df

    # Aggregate df
    metrics = ['Revenue (M u)', 'Revenues (M €)', 'Customers (M)']
    result = [df_1[revenue_fields['revenue']].sum()/1000000, df_1[revenue_fields['revenues']
                                                                  ].sum()/1000000, df_1[revenue_fields['num clients']].sum()/1000000]
    target = [df_1[revenue_fields['revenue target']].sum(
    )/1000000, df_1[revenue_fields['rev target']].sum()/1000000, '']
    performance = [df_1[revenue_fields['revenue']].sum()/df_1[revenue_fields['revenue target']].sum(),
                   df_1[revenue_fields['revenues']].sum()/df_1[revenue_fields['rev target']].sum(), '']
    df = pd.DataFrame({'KPI': metrics, 'Result': result,
                      'Target': target, 'Target_Percent': performance})

    # Configure table data
    data = df.to_dict('records')
    columns = [
        {'id': 'KPI', 'name': 'KPI'},
        {'id': 'Result', 'name': 'Result', 'type': 'numeric', 'format': Format(
            scheme=Scheme.fixed, precision=2, group=Group.yes, group_delimiter=',', decimal_delimiter='.')},
        {'id': 'Target', 'name': 'Target',  'type': 'numeric', 'format': Format(
            scheme=Scheme.fixed, precision=2, group=Group.yes, group_delimiter=',', decimal_delimiter='.')},
        {'id': 'Target_Percent', 'name': '% Target',
            'type': 'numeric', 'format': FormatTemplate.percentage(2)}
    ]

    # Configure conditional formatting
    conditional_style = [
        {'if': {
            'filter_query': '{Result} >= {Target} && {Target} > 0',
            'column_id': 'Target_Percent'},
         'backgroundColor': fanduel_colors['light-blue'],
         'color': fanduel_colors['dark-blue'],
         'fontWeight': 'bold'
         },
        {'if': {
            'filter_query': '{Result} < {Target} && {Target} > 0',
            'column_id': 'Target_Percent'},
         'backgroundColor': fanduel_colors['red'],
         'color': fanduel_colors['dark-blue'],
         'fontWeight': 'bold'
         },
    ]

    return data, columns, conditional_style

####################################################################################################
# 003 - REVENUE COUNT DAY
####################################################################################################


@app.callback(
    dash.dependencies.Output('revenue-count-day', 'figure'),
    [dash.dependencies.Input('date-picker-revenue', 'start_date'),
     dash.dependencies.Input('date-picker-revenue', 'end_date'),
     dash.dependencies.Input('reporting-groups-l1dropdown-revenue', 'value'),
     dash.dependencies.Input('reporting-groups-l2dropdown-revenue', 'value')])
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
        revenue_df_1 = revenue_import.loc[revenue_import[revenue_fields['reporting_group_l1']].isin(
            reporting_l1_dropdown), :].copy()
    else:
        revenue_df_1 = revenue_import.copy()
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
        revenue_df = revenue_df_1.loc[revenue_df_1[revenue_fields['reporting_group_l2']].isin(
            reporting_l2_dropdown), :].copy()
    else:
        revenue_df = revenue_df_1.copy()
    del revenue_df_1

    # Aggregate df
    val_cols = [revenue_fields['revenue'], revenue_fields['revenue target']]
    revenue_df = revenue_df.groupby(revenue_fields['date'])[
        val_cols].agg('sum')
    revenue_df.reset_index(inplace=True)

    # Filter based on the date filters
    df = revenue_df.loc[(revenue_df[revenue_fields['date']] >= start) & (
        revenue_df[revenue_fields['date']] <= end), :].copy()
    del revenue_df

    # Build graph
    hovertemplate_xy = (
        "<i>Day</i>: %{x|%a, %d-%b-%Y}<br>" +
        "<i>Revenue</i>: %{y:,d}" +
        "<extra></extra>")  # Remove trace info
    data = go.Scatter(
        x=df[revenue_fields['date']],
        y=df[revenue_fields['revenue']],
        line={'color': fanduel_colors['light-blue'], 'width': 0.5},
        hovertemplate=hovertemplate_xy)
    fig = go.Figure(data=data, layout=fanduel_layout)
    fig.update_layout(
        title={'text': "Revenue per Day"},
        xaxis={
            'title': "Day",
            'tickformat': "%d-%m-%y"},
        yaxis={
            'title': "Revenue (units)",
            'range': [0, 100000]},
        showlegend=False)

    return fig

####################################################################################################
# 004 - REVENUE COUNT MONTH
####################################################################################################


@app.callback(
    dash.dependencies.Output('revenue-count-month', 'figure'),
    [dash.dependencies.Input('date-picker-revenue', 'start_date'),
     dash.dependencies.Input('date-picker-revenue', 'end_date'),
     dash.dependencies.Input('reporting-groups-l1dropdown-revenue', 'value'),
     dash.dependencies.Input('reporting-groups-l2dropdown-revenue', 'value')])
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
        revenue_df_1 = revenue_import.loc[revenue_import[revenue_fields['reporting_group_l1']].isin(
            reporting_l1_dropdown), :].copy()
    else:
        revenue_df_1 = revenue_import.copy()
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
        revenue_df = revenue_df_1.loc[revenue_df_1[revenue_fields['reporting_group_l2']].isin(
            reporting_l2_dropdown), :].copy()
    else:
        revenue_df = revenue_df_1.copy()
    del revenue_df_1

    # Filter based on the date filters
    df1 = revenue_df.loc[(revenue_df[revenue_fields['date']] >= start) & (
        revenue_df[revenue_fields['date']] <= end), :].copy()
    df1['month'] = df1[revenue_fields['date']].dt.month
    del revenue_df

    # Aggregate df
    val_cols = [revenue_fields['revenue'], revenue_fields['revenue target']]
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
        y=df[revenue_fields['revenue']],
        marker={'color': fanduel_colors['light-blue'], 'opacity': 0.75},
        hovertemplate=hovertemplate_xy)
    fig = go.Figure(data=data, layout=fanduel_layout)

    # Add target% as line on secondary axis
    hovertemplate_xy2 = (
        "<i>Month</i>: %{x}<br>" +
        "<i>Target percentage</i>: %{y:%}" +
        "<extra></extra>")  # Remove trace info
    fig.add_trace(
        go.Scatter(
            x=df['month'],
            y=df[revenue_fields['revenue']] /
            df[revenue_fields['revenue target']],
            line={'color': fanduel_colors['red'], 'width': 2},
            yaxis="y2",
            opacity=0.75,
            hovertemplate=hovertemplate_xy2)
    )
    fig.update_layout(
        title={'text': "Revenue per Month vs Target"},
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
            'title': "% over Revenue target",
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
    dash.dependencies.Output('revenue-weekly-heatmap', 'figure'),
    [dash.dependencies.Input('date-picker-revenue', 'start_date'),
     dash.dependencies.Input('date-picker-revenue', 'end_date'),
     dash.dependencies.Input('reporting-groups-l1dropdown-revenue', 'value'),
     dash.dependencies.Input('reporting-groups-l2dropdown-revenue', 'value')])
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
        revenue_df_1 = revenue_import.loc[revenue_import[revenue_fields['reporting_group_l1']].isin(
            reporting_l1_dropdown), :].copy()
    else:
        revenue_df_1 = revenue_import.copy()
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
        revenue_df = revenue_df_1.loc[revenue_df_1[revenue_fields['reporting_group_l2']].isin(
            reporting_l2_dropdown), :].copy()
    else:
        revenue_df = revenue_df_1.copy()
    del revenue_df_1

    # Filter based on the date filters
    df1 = revenue_df.loc[(revenue_df[revenue_fields['date']] >= start) & (
        revenue_df[revenue_fields['date']] <= end), :].copy()
    df1['week'] = df1[revenue_fields['date']].dt.strftime("%V")
    df1['weekday'] = df1[revenue_fields['date']].dt.weekday
    del revenue_df

    # Aggregate df
    val_cols = [revenue_fields['revenue']]
    df = df1.groupby(['week', 'weekday'])[val_cols].agg('sum')
    df.reset_index(inplace=True)
    del df1

    # Build graph
    hovertemplate_here = (
        "<i>Week</i>: %{x}<br>" +
        "<i>Weekday</i>: %{y}<br>" +
        "<i>Revenue</i>: %{z}" +
        "<extra></extra>")  # Remove trace info
    data = go.Heatmap(
        x=df['weekday'],
        y=df['week'],
        z=df[revenue_fields['revenue']],
        hovertemplate=hovertemplate_here,
        hoverongaps=False,
        colorscale=fanduel_colorscale,
        showscale=False,
        xgap=1,
        ygap=1)
    fig = go.Figure(data=data, layout=fanduel_layout)
    fig.update_layout(
        title={'text': "Heatmap: Revenue by week and weekeday"},
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
# 006 - REVENUE BY COUNTRY
####################################################################################################


@app.callback(
    dash.dependencies.Output('revenue-count-country', 'figure'),
    [dash.dependencies.Input('date-picker-revenue', 'start_date'),
     dash.dependencies.Input('date-picker-revenue', 'end_date'),
     dash.dependencies.Input('reporting-groups-l1dropdown-revenue', 'value'),
     dash.dependencies.Input('reporting-groups-l2dropdown-revenue', 'value')])
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
        revenue_df_1 = revenue_import.loc[revenue_import[revenue_fields['reporting_group_l1']].isin(
            reporting_l1_dropdown), :].copy()
    else:
        revenue_df_1 = revenue_import.copy()
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
        revenue_df = revenue_df_1.loc[revenue_df_1[revenue_fields['reporting_group_l2']].isin(
            reporting_l2_dropdown), :].copy()
    else:
        revenue_df = revenue_df_1.copy()
    del revenue_df_1

    # Filter based on the date filters
    df1 = revenue_df.loc[(revenue_df[revenue_fields['date']] >= start) & (
        revenue_df[revenue_fields['date']] <= end), :].copy()
    del revenue_df

    # Aggregate df
    val_cols = [revenue_fields['revenue']]
    df = df1.groupby(revenue_fields['reporting_group_l1'])[val_cols].agg('sum')
    df.reset_index(inplace=True)
    df.sort_values(revenue_fields['reporting_group_l1'], axis=0,
                   ascending=True, inplace=True, na_position='last')
    del df1

    # Prepare incr % data
    hover_text = []
    sale_perc = []
    sale_base = [0]
    sale_b = 0
    revenue_tot = df[revenue_fields['revenue']].sum()
    for index, row in df.iterrows():
        sale_p = row[revenue_fields['revenue']]/revenue_tot
        hover_text.append(("<i>Country</i>: {}<br>" +
                           "<i>Revenue</i>: {:.2%}" +
                           "<extra></extra>").format(row[revenue_fields['reporting_group_l1']],
                                                     sale_p))
        sale_b = sale_b + sale_p
        sale_perc.append(sale_p)
        sale_base.append(sale_b)
    sale_base = sale_base[:-1]
    df['sale_p'] = sale_perc
    df['hovertext'] = hover_text

    # Build graph
    data = go.Bar(
        x=df[revenue_fields['reporting_group_l1']],
        y=df['sale_p'],
        base=sale_base,
        marker={'color': fanduel_colors['light-blue'],
                'opacity': 0.75},
        hovertemplate=df['hovertext'])
    fig = go.Figure(data=data, layout=fanduel_layout)
    fig.update_layout(
        title={'text': "Revenue Percentage by Country"},
        xaxis={'title': "Country", 'tickangle': 0},
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
    dash.dependencies.Output('revenue-bubble-county', 'figure'),
    [dash.dependencies.Input('date-picker-revenue', 'start_date'),
     dash.dependencies.Input('date-picker-revenue', 'end_date'),
     dash.dependencies.Input('reporting-groups-l1dropdown-revenue', 'value'),
     dash.dependencies.Input('reporting-groups-l2dropdown-revenue', 'value')])
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
        revenue_df_1 = revenue_import.loc[revenue_import[revenue_fields['reporting_group_l1']].isin(
            reporting_l1_dropdown), :].copy()
    else:
        revenue_df_1 = revenue_import.copy()
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
        revenue_df = revenue_df_1.loc[revenue_df_1[revenue_fields['reporting_group_l2']].isin(
            reporting_l2_dropdown), :].copy()
    else:
        revenue_df = revenue_df_1.copy()
    del revenue_df_1

    # Filter based on the date filters
    df1 = revenue_df.loc[(revenue_df[revenue_fields['date']] >= start) & (
        revenue_df[revenue_fields['date']] <= end), :].copy()
    del revenue_df

    # Aggregate df
    val_cols = [revenue_fields['revenue'],
                revenue_fields['num clients'], revenue_fields['revenues']]
    df = df1.groupby(revenue_fields['reporting_group_l1'])[val_cols].agg('sum')
    df.reset_index(inplace=True)
    df['rev_per_cl'] = df[revenue_fields['revenues']] / \
        df[revenue_fields['num clients']]
    del df1

    # Build graph
    # Add hover text info on the df
    hover_text = []
    for index, row in df.iterrows():
        hover_text.append(('<i>Country</i>: {}<br>' +
                          '<i>Revenue</i>: {:,d}<br>' +
                           '<i>Clients</i>: {:,d}<br>' +
                           '<i>Revenues</i>: {:,d}' +
                           '<extra></extra>').format(row[revenue_fields['reporting_group_l1']],
                                                     row[revenue_fields['revenue']],
                                                     row[revenue_fields['num clients']],
                                                     row[revenue_fields['revenues']]))
    df['hovertext'] = hover_text
    sizeref = 2.*max(df[revenue_fields['revenue']])/(100**2)

    # Create bubbles (1 color per country, one trace per city)
    country_names = sorted(df[revenue_fields['reporting_group_l1']].unique())
    countries = len(country_names)
    colorscale = colorscale_generator(n=countries, starting_col={
                                      'r': 57, 'g': 81, 'b': 85}, finish_col={'r': 251, 'g': 251, 'b': 252})

    fig = go.Figure(layout=fanduel_layout)
    i = 0
    for co in country_names:
        color = colorscale[i]
        i = i+1
        df_i = df.loc[df[revenue_fields['reporting_group_l1']] == co, :].copy()
        fig.add_trace(
            go.Scatter(
                x=df_i['rev_per_cl'],
                y=df_i[revenue_fields['num clients']],
                name=co,
                hovertemplate=df_i['hovertext'],
                marker_size=df_i[revenue_fields['revenue']],
                marker={
                    'color': color,
                    'line_width': 1,
                    'line': {'color': fanduel_colors['light-grey']}
                })
        )

    fig.update_traces(mode='markers', marker={
                      'sizemode': 'area', 'sizeref': sizeref})
    fanduel_margins_here = fanduel_margins
    fanduel_margins_here['t'] = 65
    fig.update_layout(
        title={'text': "Revenue per Client by Country"},
        xaxis={'title': "Revenue per Client", 'tickangle': 0},
        yaxis={'title': "Revenue (Units)"},
        margin=fanduel_margins_here)

    return fig

####################################################################################################
# 008 - REVENUE BY COUNTRY & CITY
####################################################################################################


@app.callback(
    dash.dependencies.Output('revenue-count-city', 'figure'),
    [dash.dependencies.Input('date-picker-revenue', 'start_date'),
     dash.dependencies.Input('date-picker-revenue', 'end_date'),
     dash.dependencies.Input('reporting-groups-l1dropdown-revenue', 'value'),
     dash.dependencies.Input('reporting-groups-l2dropdown-revenue', 'value')])
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
        revenue_df_1 = revenue_import.loc[revenue_import[revenue_fields['reporting_group_l1']].isin(
            reporting_l1_dropdown), :].copy()
    else:
        revenue_df_1 = revenue_import.copy()
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
        revenue_df = revenue_df_1.loc[revenue_df_1[revenue_fields['reporting_group_l2']].isin(
            reporting_l2_dropdown), :].copy()
    else:
        revenue_df = revenue_df_1.copy()
    del revenue_df_1

    # Filter based on the date filters
    df1 = revenue_df.loc[(revenue_df[revenue_fields['date']] >= start) & (
        revenue_df[revenue_fields['date']] <= end), :].copy()
    del revenue_df

    # Aggregate df
    val_cols = [revenue_fields['revenue'], revenue_fields['revenue target']]
    df = df1.groupby([revenue_fields['reporting_group_l1'],
                     revenue_fields['reporting_group_l2']])[val_cols].agg('sum')
    df.reset_index(inplace=True)
    # Include hover data
    hover_text = []
    for index, row in df.iterrows():
        hover_text.append(("<i>Country</i>: {}<br>" +
                           "<i>City</i>: {}<br>" +
                           "<i>Revenue</i>: {:,d}<br>" +
                           "<i>Targets</i>: {:,d}" +
                           "<extra></extra>").format(row[revenue_fields['reporting_group_l1']],
                                                     row[revenue_fields['reporting_group_l2']],
                                                     row[revenue_fields['revenue']],
                                                     row[revenue_fields['revenue target']]))
    df['hovertext'] = hover_text
    df['l1l2'] = df[revenue_fields['reporting_group_l1']] + \
        "_" + df[revenue_fields['reporting_group_l2']]
    # Generate colors
    ncolors = len(df[revenue_fields['reporting_group_l2']].unique())
    colorscale = colorscale_generator(n=ncolors)

    # Build graph
    data = []
    i = 0
    for l in sorted(df['l1l2']):
        df_l = df.loc[(df['l1l2'] == l), :].copy()
        trace = go.Bar(
            name=l,
            x=df_l[revenue_fields['reporting_group_l1']],
            y=df_l[revenue_fields['revenue']],
            hovertemplate=df_l['hovertext'],
            marker={
                'color': colorscale[i],
                'opacity': 0.85,
                'line_width': 1,
                'line': {'color': colorscale[i]}
            }
        )
        i = i+1
        data.append(trace)
    fig = go.Figure(data=data, layout=fanduel_layout)
    fig.update_layout(
        barmode='stack',
        title={'text': "Revenue by Country & City"},
        xaxis={'title': "Country", 'tickangle': 0},
        yaxis={'title': "Revenue (Units)"},
        showlegend=False)

    return fig
