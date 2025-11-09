# pages/arena_comparison.py
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/arena", name="Arena Comparison")

layout = dbc.Container(
    [
        html.H2("Arena 1 vs Arena 2"),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Arena 1 Overview"),
                    dbc.CardBody([
                        dcc.Graph(
                            figure={"data": [], "layout": {"title": "Arena 1 Performance"}}
                        ),
                        dbc.Button("Load Arena 1 Data", color="info", className="mt-2")
                    ])
                ])
            ], md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Arena 2 Overview"),
                    dbc.CardBody([
                        dcc.Graph(
                            figure={"data": [], "layout": {"title": "Arena 2 Performance"}}
                        ),
                        dbc.Button("Load Arena 2 Data", color="secondary", className="mt-2")
                    ])
                ])
            ], md=6),
        ]),
    ],
    fluid=True,
)
