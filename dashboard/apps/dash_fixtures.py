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

from dashboard_data import DataInit
df_teams = init.team_names()
df_fixture_form = init.fixture_form_decending('Arsenal')


layout = html.Div([
        dbc.Row([
            dbc.Col(
                dash_table.DataTable(
                    id='data-table-graph',
                    # editable=True,
                    data=df_fixture_form.to_dict('records'),
                    columns=[{'id': c, 'name': c} for c in df_fixture_form.columns],
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

       ])

	]),

@app.callback(
    Output('data-table-graph', 'columns'),
    [Input(str(i), 'n_clicks') for i in df_teams['teams']]
)
def columns_form_five(*args):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    team = changed_id.split('.')[0]
    df = init.fixture_form_decending(team)
    data=df.to_dict('records')
    columns=[{'id': c, 'name': c} for c in df.columns]
    return columns

@app.callback(
    Output('data-table-graph', 'data'),
    [Input(str(i), 'n_clicks') for i in df_teams['teams']]
)
def data_form_five(*args):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    team = changed_id.split('.')[0]
    df = init.fixture_form_decending(team)
    data=df.to_dict('records')
    columns=[{'id': c, 'name': c} for c in df.columns]
    return data