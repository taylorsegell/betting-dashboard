from dash import dcc, html
import dash

from app import app
from app import server
from layouts import revenue, page2, page3
#import callbacks
import YEAH

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/revenue-overview':
        return revenue
    elif pathname == '/apps/page2':
        return page2
    elif pathname == '/apps/page3':
        return page3
    else:
        return revenue  # This is the "home page"


if __name__ == '__main__':
    app.run_server(dev_tools_hot_reload=True, dev_tools_ui=True, debug=False)
