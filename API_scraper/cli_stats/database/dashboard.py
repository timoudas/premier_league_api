# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table

from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

import pandas as pd

from mongo_query import DB
from pprint import pprint

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

stats_param = [{'label': 'Fixture Stats', 'value':'FS'},
                   {'label': 'Player Stats', 'value':'PS'},
                   {'label': 'Team Standings', 'value':'TS'}]

year_param = [{'label': '2019/2020', 'value':'2019'},
                   {'label': '2018/2019', 'value':'2018'},]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div([

    html.Div(
        [
            dcc.Dropdown(
                id='data_param_dd',
                options=stats_param,
                value='FS',
                style = {'width':'40%',}
            ),

            dcc.Dropdown(
                id='year_param_dd',
                options=year_param,
                value='2019',
                style = {'width':'40%',}
            ),
        ],
    ),

    html.Div(
        id='dd-output-container',
    )
])

@app.callback(

    dash.dependencies.Output('dd-output-container', 'children'),

    [
        dash.dependencies.Input('data_param_dd', 'value'),
        dash.dependencies.Input('year_param_dd', 'value'),
    ]
)

def update_output(data, year):
    instance = DB('EN_PR', year)
    cmd = {'FS': 'get_fixtures',
           'PS': 'get_players', 
           'TS': 'get_teams_standing'}
    command = cmd.get(data)
    query = getattr(instance, command)()
    df = pd.DataFrame.from_dict(query)
    df = df.drop('_id', 1)
    columns = [{'name': col, 'id': col} for col in df.columns]
    data = df.to_dict('records')
    return [dash_table.DataTable(
                data=data, 
                columns=columns,
                style_cell={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                },
                fixed_rows={
                    'headers': True
                },
                style_table={
                    'height': '300px', 
                    'overflowY': 'auto'
                },
            )]


if __name__ == '__main__':
    app.run_server(debug=True)