# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px

from functools import lru_cache

import dash_bootstrap_components as dbc


from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

import pandas as pd

from mongo_query import DB
from pprint import pprint

"""
if command == 'get_teams_standing':
      data = df.to_dict('records')
      availible_teams = df['team_shortName'].unique()
      fig = px.line(df, x="gameweek", y="points", 
                    hover_name="team_shortName", color="team_shortName")
      fig.update_xaxes(rangeslider_visible=True,)
"""

def init_data():
    query = DB('EN_PR', '2019').get_teams_standing()
    df = pd.DataFrame.from_dict(query)
    df = df.drop('_id', 1)
    return df

df = init_data()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

stats_param = [{'label': 'Fixture Stats', 'value':'FS'},
                   {'label': 'Player Stats', 'value':'PS'},
                   {'label': 'Team Standings', 'value':'TS'}]

year_param = [{'label': '2019/2020', 'value':'2019'},
                   {'label': '2018/2019', 'value':'2018'}]


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div(
    [
        dbc.Jumbotron([
            dbc.Container([
                html.H1("Premier League Dashboard", className="display-3"),
                html.P(
                    "View all the the stats from the Premier"
                    "League",
                    className="lead",
                ),
                html.P(
                    "Availible: Player stats, Team Standings, "
                    "Fixture Stats",
                    className="lead",
                ),
            ],
            fluid=True,
            ),
        ],
        fluid=True,
        ),

        dbc.Row([
                dbc.Col([
                    dbc.Select(
                        options=stats_param,
                        id='data_param_dd',
                        value='TS'
                    ),
                ], width=2),

                dbc.Col([
                    dbc.Select(
                        options=year_param,
                        id='year_param_dd',
                        value='2019'
                    ),
                    dbc.Button(
                        "Submit", 
                        color="primary", 
                        className="mr-1",
                        id='params-button',
                        block=True
                    ),

                ], width=2),

                dbc.Col(
                    dash_table.DataTable(
                        id = 'table',
                        data = df.to_dict('records'),
                        columns = [{"name": i, "id": i} for i in df.columns],
                        style_table={
                            'overflowX': 'auto',
                            'height': '300px', 
                            'overflowY': 'auto'
                        },
                    ),
                width=8,
            ),

        ]),
        dbc.Row([

        ]),

    ],
)
@app.callback(

        Output('table', 'data'),
    [
        Input('params-button', 'n_clicks'),
    ],
    [
        State('data_param_dd', 'value'),
        State('year_param_dd', 'value')
    ]
)
@lru_cache(maxsize=32)
def update_output(n_clicks, data, year):
    print('making call')
    instance = DB('EN_PR', year)
    cmd = {'FS': 'get_fixtures',
           'PS': 'get_players', 
           'TS': 'get_teams_standing'}
    command = cmd.get(data)
    query = getattr(instance, command)()
    df = pd.DataFrame.from_dict(query)
    df = df.drop('_id', 1)
    print('returning...')
    print(df)
    return [{
          'data': df.to_dict('records'),
          'columns' : [{"name": i, "id": i} for i in df.columns],
        }]

if __name__ == '__main__':
    app.run_server(debug=True)