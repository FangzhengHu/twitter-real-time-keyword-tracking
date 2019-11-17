# ref: https://dash.plot.ly/live-updates
import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Real Time Twitter Keyword Tracker'

app.layout = html.Div(children=[
    html.H2('Real-time Twitter Keyword Tracker for Brand Analytics', style={
        'textAlign': 'center'
    }),

    html.Div(id='last-updated-time', style={
        'textAlign': 'center'
    }),

    dcc.Interval(
        id='interval-component',
        interval=1*1000,  # in milliseconds
        n_intervals=0
    )
])


@app.callback(Output('last-updated-time', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_time(n):
    return f'(Last updated at {datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")})'


if __name__ == '__main__':
    app.run_server(debug=True)
