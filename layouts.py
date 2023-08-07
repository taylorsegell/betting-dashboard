from dash import dcc, html, dash_table
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
import dash
from dash.dash_table.Format import Format, Group, Scheme
from datetime import datetime as dt
from app import app

####################################################################################################
# 000 - FORMATTING INFO
####################################################################################################

# Corporate css formatting
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

externalgraph_rowstyling = {
    'margin-left': '15px',
    'margin-right': '15px',
    'padding': '1rem 0rem'
}

externalgraph_colstyling = {
    'border-radius': '10px',
    'border-style': 'solid',
    'border-width': '1px',
    'border-color': account_colors['superdark-blue'],
    'background-color': account_colors['superdark-blue'],
    'box-shadow': '0px 0px 17px 0px #CFD6DB',
    'padding-top': '10px'
}

filterdiv_borderstyling = {
    'border-radius': '0px 0px 10px 10px',
    'border-style': 'solid',
    'border-width': '1px',
    'border-color': account_colors['light-blue'],
    'background-color': account_colors['superdark-blue'],
    'box-shadow': '2px 5px 5px 1px #445058'
}

navbarcurrentpage = {
    'text-decoration': 'underline',
    'background-image': 'linear-gradient(#484e55, #3a3f44 60%, #313539)',
    'border-radius': '4px',
    ' border': '0.5px solid #1b1e20',
    'text-shadow': '0px 0px 1px #FFFFFF'
}

rfmdiv = {
    'display': 'flex',
    'flex-direction': 'column',
    'text-align': 'center',
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
    'color': account_colors['white'],
    'font-size': '1.5rem',
    'letter-spacing': '0.04em'
}

# Corporate chart formatting

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

account_layout = go.Layout(
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
account_layout2 = go.Layout(
    font={'family': account_font_family, 'color': '#ffffff'},
    title=account_title,
    title_x=0.5,  # Align chart title to center
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    xaxis=account_xaxis,
    yaxis=account_yaxis,
    legend=account_legend,
    margin=account_margins
)


<<<<<<< HEAD
dropdown_format = {'font-size': '13px',"background-color":"#1f375b",
=======
dropdown_format = {'font-size': '13px',
>>>>>>> 19b613e (First Commit)
                   'color': account_colors['medium-blue-grey'], 'white-space': 'nowrap', 'text-overflow': 'ellipsis'}
####################################################################################################
# 000 - DATA MAPPING
####################################################################################################
df = pd.read_pickle('finalpickle.pkl')
groupdf = df.groupby(['placed_date', 'state', 'sport']).agg({'wagerid': 'count', 'playerid': pd.Series.nunique, 'decimal_odds': np.mean, 'gross_revenue': [
    np.mean, np.sum], 'rfm_score': np.mean, 'recency': np.mean, 'frequency': np.mean, 'rfm_segment': pd.Series.mode}).reset_index()
groupdf.sort_values(['placed_date', 'state', 'sport'], inplace=True)
groupdf.columns = groupdf.columns.map('|'.join).str.strip(
    '|').str.replace('[|_]', ' ', regex=True).str.title()
new_df = groupdf.rename(columns={'Wagerid Count': 'Wagers',
                        'Playerid Nunique': 'Players', 'Rfm Score Mean': 'RFM Score Mean'})


sp = ['All',
      'NFL',
      'MLB',
      'NBA',
      'NHL',
      'College Football',
      'College Basketball',
      'Champions League']

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

####################################################################################################
# 000 - IMPORT DATA
####################################################################################################

###########################


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
# 000 - DEFINE REUSABLE COMPONENTS AS FUNCTIONS
####################################################################################################

#####################
# Header with logo


def get_header():

    header = html.Div([

        # Same as img width, allowing to have the title centrally aligned
        html.Div([], className='col-2'),

        html.Div([
            html.H1(children='Performance Dashboard',
                    style={'textAlign': 'center'}
                    )],
                 className='col-8',
                 style={'padding-top': '1%'}
                 ),

        html.Div([
            html.Img(
                src=app.get_asset_url('logo_001c.png'),
                height='43 px',
                width='auto')
        ],
            className='col-2',
            style={
            'align-items': 'center',
            'padding-top': '1%',
            'height': 'auto'})

    ],
        className='row',
        style={'height': '4%',
               'background-color': account_colors['superdark-blue']}
    )
    html.Div([  # Internal row - RECAPS

                # html.Div([], className='col-4'),  # Empty column

                html.Div([
                    dash_table.DataTable(
                        id='recap-table',
                        style_header={
                            'backgroundColor': 'transparent',
                            'fontFamily': account_font_family,
                            'font-size': '1.25rem',
                            'color': account_colors['white'],
                            'border': '0px transparent',
                            'textAlign': 'center',
                            'minWidth': '180px', 'width': '180px', 'maxWidth': '180px'},
                        style_cell={
                            'backgroundColor': 'transparent',
                            'fontFamily': account_font_family,
                            'font-size': '1rem',
                            'color': account_colors['white'],
                            'border': '0px transparent',
                            'textAlign': 'center',
                            'minWidth': '180px', 'width': '180px', 'maxWidth': '180px'},
                        cell_selectable=False,
                        column_selectable=False
                    )
                ],
                    className='col-12'),

        # html.Div([], className='col-4')  # Empty column

    ],
        className='row',
        style=recapdiv
    ),  # Internal row - RECAPS

    return header

#####################
# Nav bar


def get_navbar(p='revenue'):

    navbar_revenue = html.Div([

        html.Div([], className='col-3'),

        html.Div([
            dcc.Link(
                html.H4(children='Overview',
                        style=navbarcurrentpage),
                href='/apps/revenue-overview'
            )
        ],
            className='col-2'),

        html.Div([
            dcc.Link(
                html.H4(children='Sport Focused'),
                href='/apps/page2'
            )
        ],
            className='col-2'),

        html.Div([
            dcc.Link(
                html.H4(children='Segementation'),
                href='/apps/page3'
            )
        ],
            className='col-2'),

        html.Div([], className='col-3')

    ],
        className='row',
        style={'background-color': account_colors['dark-blue'],
               'box-shadow': '2px 5px 5px 1px #445058'}
    )

    navbar_page2 = html.Div([

        html.Div([], className='col-3'),

        html.Div([
            dcc.Link(
                html.H4(children='GGR'),
                href='/apps/revenue-overview'
            )
        ],
            className='col-2'),

        html.Div([
            dcc.Link(
                html.H4(children='GGR Focus',
                        style=navbarcurrentpage),
                href='/apps/page2'
            )
        ],
            className='col-2'),

        html.Div([
            dcc.Link(
                html.H4(children='Segementation'),
                href='/apps/page3'
            )
        ],
            className='col-2'),

        html.Div([], className='col-3')

    ],
        className='row',
        style={'background-color': account_colors['dark-blue'],
               'box-shadow': '2px 5px 5px 1px #445058'}
    )

    navbar_page3 = html.Div([

        html.Div([], className='col-3'),

        html.Div([
            dcc.Link(
                html.H4(children='GGR'),
                href='/apps/revenue-overview'
            )
        ],
            className='col-2'),

        html.Div([
            dcc.Link(
                html.H4(children='GGR Focus'),
                href='/apps/page2'
            )
        ],
            className='col-2'),

        html.Div([
            dcc.Link(
                html.H4(children='Segementation',
                        style=navbarcurrentpage),
                href='/apps/page3'
            )
        ],
            className='col-2'),

        html.Div([], className='col-3')

    ],
        className='row',
        style={'background-color': account_colors['dark-blue'],
               'box-shadow': '2px 5px 5px 1px #445058'}
    )

    if p == 'revenue':
        return navbar_revenue
    elif p == 'page2':
        return navbar_page2
    else:
        return navbar_page3

#####################
# Empty row


def get_emptyrow(h='45px'):
    """This returns an empty row of a defined height"""

    emptyrow = html.Div([
        html.Div([
            html.Br()
        ], className='col-12')
    ],
        className='row',
        style={'height': h})

    return emptyrow

####################################################################################################
# 001 - REVENUE
####################################################################################################


revenue = html.Div([

    #####################
    # Row 1 : Header
    get_header(),

    #####################
    # Row 2 : Nav bar
    get_navbar('revenue'),

    #####################
    # Row 3 : Filters
    html.Div([  # External row

        html.Div([  # External 12-column

            html.Div([  # Internal row

                # Internal columns
                html.Div([
                ],
                    className='col-2'),  # Blank 2 columns

                # Filter pt 1
                html.Div([

                    html.Div([
                        html.H5(
                            children='Filters by Date:',
                            style={'text-align': 'left',
                                   'color': account_colors['medium-blue-grey']}
                        ),
                        # Date range picker
                        html.Div(['Select a date range: ',
                                  dcc.DatePickerRange(
                                      id='date-picker-revenue',
                                      start_date=min_dt_str,
                                      end_date=max_dt_str,
                                      min_date_allowed=min_dt,
                                      max_date_allowed=max_dt,
                                      start_date_placeholder_text='Start date',
                                      display_format='DD-MMM-YYYY',
                                      first_day_of_week=1,
                                      end_date_placeholder_text='End date',
                                      style={'font-size': '12px', 'display': 'inline-block', 'border-radius': '2px', 'border': '1px solid #ccc', 'color': '#333', 'border-spacing': '0', 'border-collapse': 'separate'})
                                  ], style={'margin-top': '5px', 'color': 'medium-blue-grey'}
                                 )

                    ],
                        style={'margin-top': '10px',
                               'margin-bottom': '5px',
                               'text-align': 'left',
                               'paddingLeft': 5})

                ],
                    className='col-4'),  # Filter part 1

                # Filter pt 2
                html.Div([

                    html.Div([
                        html.H5(
                            children='Filters by Reporting Groups:',
                            style={'text-align': 'left',
                                   'color': account_colors['medium-blue-grey']}
                        ),
                        # Reporting group selection l1
                        html.Div([
                            dcc.Dropdown(id='reporting-groups-l1dropdown-revenue',
                                         options=state_all,
                                         value=[''],
                                         multi=True,
                                         placeholder="Select " + \
                                         'State' + \
                                         " (leave blank to include all)",
                                         style=dropdown_format)
                        ],
                            style={'width': '70%', 'margin-top': '5px'}),
                        # Reporting group selection l2
                        html.Div([
                            dcc.Dropdown(id='reporting-groups-l2dropdown-revenue',
                                         options=sports_all_2,
                                         value=[''],
                                         multi=True,
                                         placeholder="Select " + \
                                         'Sport' + \
                                         " (leave blank to include all)",
                                         style=dropdown_format)
                        ],
                            style={'width': '70%', 'margin-top': '5px'})
                    ],
                        style={'margin-top': '10px',
                               'margin-bottom': '5px',
                               'text-align': 'left',
                               'paddingLeft': 5})

                ],
                    className='col-4'),  # Filter part 2

                html.Div([
                ],
                    className='col-2')  # Blank 2 columns


            ],
                className='row')  # Internal row

        ],
            className='col-12',
            style=filterdiv_borderstyling)  # External 12-column

    ],
        className='row sticky-top'),  # External row

    #####################
    # Row 4
    get_emptyrow(),

    #####################
    # Row 5 : Charts
    html.Div([  # External row

        html.Div([
        ],
            className='col-1'),  # Blank 1 column

        html.Div([  # External 10-column

            html.H2(children="Past Year KPIs",
                    style={'color': account_colors['white']}),

            html.Div([  # Internal row - RECAPS

                # html.Div([], className='col-4'),  # Empty column

                html.Div([
                    dash_table.DataTable(
                        id='recap-table',
                        style_header={
                            'backgroundColor': 'transparent',
                            'fontFamily': account_font_family,
                            'font-size': '1.25rem',
                            'color': account_colors['white'],
                            'border': '0px transparent',
                            'textAlign': 'center',
                            'minWidth': '180px', 'width': '180px', 'maxWidth': '180px'},
                        style_cell={
                            'backgroundColor': 'transparent',
                            'fontFamily': account_font_family,
                            'font-size': '1rem',
                            'color': account_colors['white'],
                            'border': '0px transparent',
                            'textAlign': 'center',
                            'minWidth': '180px', 'width': '180px', 'maxWidth': '180px'},
                        cell_selectable=False,
                        column_selectable=False
                    )
                ],
                    className='col-12'),

                # html.Div([], className='col-4')  # Empty column

            ],
                className='row',
                style=recapdiv
            ),  # Internal row - RECAPS

            html.Div([  # Internal row

                # Chart Column
                html.Div([
                    dcc.Graph(
                        id='revenue-count-day')
                ],
                    className='col-4'),

                # Chart Column
                html.Div([
                    dcc.Graph(
                        id='revenue-count-month')
                ],
                    className='col-4'),

                # Chart Column
                html.Div([
                    dcc.Graph(
                        id='revenue-weekly-heatmap')
                ],
                    className='col-4')

            ],
                className='row'),  # Internal row

            html.Div([  # Internal row

                # Chart Column
                html.Div([
                    dcc.Graph(
                        id='revenue-count-state')
                ],
                    className='col-4'),

                # Chart Column
                html.Div([
                    dcc.Graph(
                        id='revenue-bubble-county')
                ],
                    className='col-4'),

                # Chart Column
                html.Div([
                    dcc.Graph(
                        id='revenue-count-sport')
                ],
                    className='col-4')

            ],
                className='row',
                style=externalgraph_rowstyling),  # Internal row


        ],
            className='col-10',
            style=externalgraph_colstyling),  # External 10-column

        get_emptyrow(),
        html.Img(src='assets/logos/01-logo/account-horizontal-logo.png',
                 style={'padding': '1rem 0rem'}),
        get_emptyrow(),
        # Blank 1 column


    ],
        className='row',
        style=externalgraph_rowstyling
    ),  # External row

])

####################################################################################################
# 002 - GGR Focus
####################################################################################################

page2 = html.Div(children=[

    #####################
    # Row 1 : Header
    get_header(),

    #####################
    # Row 2 : Nav bar
    get_navbar('page2'),

    #####################
    # Row 3 : Filters
    html.Div([  # External row

        html.Br()

    ],
        className='row sticky-top'),  # External row

    #####################
    # Row 4
    # get_emptyrow(),

    #####################
    # Row 5 : Charts
    html.Div([  # External row
        html.Div([
        ],
            className='col-1'),  # Blank 1 column

        html.Div(children=[  # External 10-column

            html.H2(children="Gross Gaming Revenue",
                    style={'color': account_colors['white']}),
            html.Div([  # Internal row - RECAPS

                        html.Div([], className='col-1'),  # Empty Col
                        html.Div([
                            html.Div([
                                html.Div([html.H5("Time Period"),
                                          dcc.RadioItems(
                                    id="period",
                                    options=[
                                        {'label': 'Month  ', 'value': 'monthname'},
                                        {'label': 'Day of Month  ',
                                         'value': 'placed_day_month'},
                                        {'label': 'Weekday  ', 'value': 'dayname'},
                                    ],
                                    value='monthname',
                                    inline=True
                                ),
                                ], className='col-6'),
                                html.Div([
                                    html.H5("Sport"),
                                    dcc.Dropdown(
                                        id="sports",
                                        options=[{'label': s, 'value': s}
                                                 for s in sp],
                                        value="All",
                                        clearable=False,
                                        style=dropdown_format
                                    ),
                                ], style={'width': '70%', 'margin-top': '5px'},
                                    className='col-6'),
                            ], className='row'),
                        ], className='col-10'),

                html.Div([], className='col-1')  # Empty Col
            ],
                className='row',
                style=recapdiv
            ),  # Internal row - RECAPS

            html.Div([  # Internal row

                        # Chart Column
                        html.Div([
                            dcc.Graph(
                                id='rev-graph',
                                style={'height': '35rem'}),
                        ],
                            className='col-12'),


            ],
                className='row'),
        ],
            className='col-10',
            style=externalgraph_colstyling),  # External 10-column

        html.Div([
        ],
            className='col-1'),  # Blank 1 column

    ],
        className='row',
        style=externalgraph_rowstyling
    ),  # External row

])
####################################################################################################
# 003 - Segementation
####################################################################################################


page3 = html.Div(children=[

    #####################
    # Row 1 : Header
    get_header(),

    #####################
    # Row 2 : Nav bar
    get_navbar('page3'),

    #####################
    # Row 3 : Filters
    html.Div([  # External row

        html.Br()

    ],
        className='row sticky-top'),  # External row

    #####################
    # Row 4
    # get_emptyrow(),

    #####################
    # Row 5 : Charts
    html.Div([  # External row

        html.Div(children=[  # External 10-column

            html.Div([
                html.Div([
                    html.H2(children="Recency, Frequency, Monetary Value",
                            style={'textAlign': 'center', 'color': account_colors['white']}),
                    html.Div([], className='col-1')  # Empty Col
                ],
                    className='row',
                    style=rfmdiv
                ),  # Internal row - RECAPS

                html.Div([
                    html.Div([
                        dcc.RadioItems(
                            id="cohorts",
                            options=[
                                {'label': 'Retention Rate ',
                                 'value': 'cohort_retention'},
                                {'label': 'Size  ',
                                 'value': 'cohort_size'}
                            ],
                            value='cohort_retention',
                            inline=True
                        ),

                        # Chart Column
                        html.Div([
                            html.H5("Average Retention by Cohort", style={
                                    'textAlign': 'center', 'padding-left': '8rem', 'margin-bottom': '-2rem'}),
                            dcc.Graph(id='retention-graph',
                                      style={'display': 'flex', 'height': '65%', 'width': '90%'})
                        ],

                            className='page-three'),
                    ], className='col-6'),

                    html.Div([

                        dcc.Dropdown(
                            id="col1",
                            options=[
                                {'label': 'Sports',
                                 'value': 'sports'},
                                {'label': 'States  ',
                                 'value': 'states'}
                            ],
                            value='sports',
                            className='ddrow'
                        ),  # Internal row

                        # Chart Column
                        html.Div([
                            html.H5("Recency Frequency Groups", style={
                                    'textAlign': 'center', 'padding-left': '8rem', 'margin-bottom': '-2rem'}),
                            dcc.Graph(
                                id='treemap_rfm',
                                style={'display': 'flex', 'height': '85%', 'width': '100%'})
                        ],

                            className='page-three'),

                    ],
                        className='col-6'),
                ],
                    className='row', style={'padding': '1rem'}
                ),
            ],
                className='col-12',
                style=externalgraph_colstyling),  # External 10-column

            # Blank 1 column

        ],
            className='row',
            style=externalgraph_rowstyling
        ),  # External row

    ], style={'padding': '1rem 3rem'}),

])
