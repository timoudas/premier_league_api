# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px

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
                   {'label': '2018/2019', 'value':'2018'},]


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

app.layout = html.Div([
    html.Div([
            dcc.Dropdown(
                id='data_param_dd',
                options=stats_param,
                value='',
            ),

            dcc.Dropdown(
                id='year_param_dd',
                options=year_param,
                value='',
            ),

          dash_table.DataTable(
            id = 'table',
            data = df.to_dict('records'),
            columns = [{"name": i, "id": i} for i in df.columns],
            style_cell={
              'whiteSpace': 'normal',
              'height': 'auto',
            },
            fixed_columns={
              'headers': True,
              'data': 1
            },
            style_table={
              'height': '300px', 
              'overflowY': 'auto',
              'minWidth': '100%',
            },
          )

    ], style = {'width':'40%',}),

    html.Div([
        
        dcc.Dropdown(
          id='team',
          options=[],
        ),

        dcc.Dropdown(
          id='team_metrics',
          options=[],
        ),
    ],
    ),
])

@app.callback(

    dash.dependencies.Output('table', 'data'),
    [
        dash.dependencies.Input('data_param_dd', 'value'),
        dash.dependencies.Input('year_param_dd', 'value'),
    ]
)
def update_output(data, year):
  if data and year:
    instance = DB('EN_PR', year)
    cmd = {'FS': 'get_fixtures',
           'PS': 'get_players', 
           'TS': 'get_teams_standing'}
    command = cmd.get(data)
    query = getattr(instance, command)()
    df = pd.DataFrame.from_dict(query)
    df = df.drop('_id', 1)
    return [{
      'data': df.to_dict('records'),
      'columns' : [{"name": i, "id": i} for i in df.columns],
    }]
  else:
    pass
    


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)