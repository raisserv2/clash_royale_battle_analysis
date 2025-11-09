# pages/player_comparison.py
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/player", name="Player Comparison")

layout = dbc.Container(
    [
        html.H2("Player 1 vs Player 2"),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Player 1 Stats"),
                    dbc.CardBody([
                        dcc.Graph(
                            figure={"data": [], "layout": {"title": "Player 1 Performance"}}
                        ),
                        dbc.Button("Load Player 1 Data", color="info", className="mt-2")
                    ])
                ])
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Player 2 Stats"),
                    dbc.CardBody([
                        dcc.Graph(
                            figure={"data": [], "layout": {"title": "Player 2 Performance"}}
                        ),
                        dbc.Button("Load Player 2 Data", color="secondary", className="mt-2")
                    ])
                ])
            ], md=6),
        ]),
    ],
    fluid=True,
)
