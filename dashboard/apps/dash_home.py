import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px

import dash_bootstrap_components as dbc


from dash.dependencies import Input
from dash.dependencies import Output
from dash.dependencies import State

import pandas as pd

from app import app
from dashboard_data import DataInit

init = DataInit()

df_teams = init.team_names()
df_standings = init.league_standings()
team_series = pd.Series(df_teams['teams'])


def gen_team_button(team_shortName):
    return dbc.Button(
                str(team_shortName),
                className="btn btn-primary",
                id=str(team_shortName),
                style={
                "margin-right": "10px",
                "margin-bottom": '10px',
                },
                n_clicks=0,

            )
def gen_latest_fixtures(team_shortName, limit=5):
    #TODO gen html.tr elems to put data in a decending order
    pass


def gen_inputs(value, i_type):
    return Input(str(value), i_type)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

stats_param = [{'label': 'Fixture Stats', 'value':'FS'},
                   {'label': 'Player Stats', 'value':'PS'},
                   {'label': 'Team Standings', 'value':'TS'}]

year_param = [{'label': '2019/2020', 'value':'2019'},
                   {'label': '2018/2019', 'value':'2018'}]

layout = html.Div(
    [
  
        dbc.Row([
	        dbc.Row([

	                dbc.Col([
	                    dbc.Select(
	                        options=stats_param,
	                        id='data_param_dd',
	                        value='TS',
	                        style = {'width': '46%', 'margin-right': '6px'}
	                    ),

	                    dbc.Select(
	                        options=year_param,
	                        id='year_param_dd',
	                        value='2019',
	                        style = {'width': '44%', 'margin-left': '6px'}
	                    ),

	                    dbc.Col(
	                        id='team-img'
	                    )

	                ], width=4),


	                dbc.Col(
	                    children=[gen_team_button(i) for i in df_teams['teams']]
	                ), 

	        ]),

	        html.Div([
	            html.Div(
	                '2019', id='intermediate-year-dd', style={'display': 'none'}, 
	            ), 
	            html.Div(
	                'TS', id='intermediate-data-dd', style={'display': 'none'}
	            ), 
	            html.Div(
	                46987, id='intermediate-f_id', style={'display': 'none'}
	            ), 
	        ]),


	        dbc.Row([
	            dbc.Col(
	                dash_table.DataTable(
	                    id='data-table-graph',
	                    # editable=True,
	                    data=df_standings.to_dict('records'),
	                    columns=[{'id': c, 'name': c} for c in df_standings.columns],
	                    style_cell_conditional=[
	                        {
	                            'if': {
	                                'column_id': 'Club'},
	                            'textAlign': 'left'
	                        },
	                        {
	                            'if': {
	                                'column_id': ['Played', 'Position']},
	                            'textAlign': 'center'
	                        },
	                    ],
	                    style_cell={'padding': '5px'},
	                    style_header={
	                        'backgroundColor': 'white',
	                        'fontWeight': 'bold',
	                    },
	                    style_as_list_view=True,
	                ),
	                width=4,
	            ),
	            dbc.Col(
	                id='league-table'
	            ),

	       ]),
       ], id='page-container'),

    ],
)

def update_img(*args):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    team = changed_id.split('.')[0]
    return html.Div([
        html.Img(src=app.get_asset_url(team + '.png'),   
            style={'position': 'absolute',
            'margin-top': '35px',
            'margin-left': '10px',}),
        html.H2(team, style={'margin-top': '40px', 'margin-left': '80px',
                            'position': 'absolute', 'color':'#6c757d',
                            'font-family': 'monospace'}),
        ], 
)

@app.callback(
        Output('intermediate-year-dd', 'children'),
    [
        Input('year_param_dd', 'value')
    ],
    )
def data_year(value):
    return value

@app.callback(
        Output('intermediate-data-dd', 'children'),
    [
        Input('data_param_dd', 'value')
    ],
)
def data_type(value):
    return value

if __name__ == '__main__':
	 app.run_server(debug=True)
