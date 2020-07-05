import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input
from dash.dependencies import Output

import dash_bootstrap_components as dbc

from app import app
from apps import dash_home


 
app.layout = html.Div([

    dcc.Location(id='url', refresh=False),
    html.Div([
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
        style={'margin-bottom': '0px'}
        ),

        dbc.Navbar(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(dbc.NavLink(
                                "Home", id='home', className="ml-2", href="/home")),
                            dbc.Col(dbc.NavLink(
                                "League", id='league', className="ml-2", href="/league", external_link=True)),
                            dbc.Col(dbc.NavLink(
                                "Teams", id='teams', className="ml-2", href="/teams", external_link=True)),
                            dbc.Col(dbc.NavLink(
                                "Fixtures", id='fitures', className="ml-2", href="/fixtures", external_link=True)),
                            dbc.Col(dbc.NavLink(
                                "Players", id='players', className="ml-2", href="/players", external_link=True)),
                        ],
                        align="center",
                        no_gutters=True,
                    ),
                ),
            ],
            color="dark",
            dark=True,
            style={'margin-bottom': '20px'},
            id='pages'

        ),

    ]),

    html.Div(id='page-content')

])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/home':
        return dash_home.serve_layout()
    elif pathname == '/league':
        return dash_league.layout
    elif pathname == '/teams':
        return dash_teams.layout
    elif pathname == '/fixtures':
        return dash_fixtures.layout
    elif pathname == '/players':
        return dash_players.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)