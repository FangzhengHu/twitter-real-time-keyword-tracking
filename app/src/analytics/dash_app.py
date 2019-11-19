# ref: https://dash.plot.ly/live-updates
import datetime
import dash
import psycopg2
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

from analyze import get_nrows, get_unique_tweet_texts, get_sentiment_polarity_df

conn = psycopg2.connect(dbname='stream_tweets')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Twitter Keyword Tracker'


app.layout = html.Div(children=[
    html.H2('Real-time Twitter Keyword Tracker for Brand Analytics',
            style={'textAlign': 'center'}),

    html.Div(id='last-updated-time', style={'textAlign': 'center'}),

    html.Div(id='tweet-count', style={'textAlign': 'center'}),

    dcc.Graph(id='sentiment-score-distribution', style={'textAlign': 'center'}),

    dcc.Interval(
        id='interval-component',
        interval=10*1000,  # in milliseconds
        n_intervals=0
    )
])


@app.callback(Output('last-updated-time', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_time(n):
    return f'(Last updated at {datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")})'


@app.callback(Output('tweet-count', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_tweet_count(n):
    tweet_count = get_nrows('tweets', conn)
    return f'Number of mentioned tweets: {tweet_count}'


@app.callback(Output('sentiment-score-distribution', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_sentiment_score_distribution(n):
    tweet_texts = get_unique_tweet_texts(conn)
    df = get_sentiment_polarity_df(tweet_texts)
    fig = px.histogram(df, 'sentiment_polarity')
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)
