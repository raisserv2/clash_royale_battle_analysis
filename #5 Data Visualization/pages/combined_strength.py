# pages/combined_strength.py
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/combined", name="Combined Strength")

layout = dbc.Container(
    [
        html.H2("Combined Strength Overview"),
        html.Hr(),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Summary Metrics"),
                    dbc.CardBody([
                        html.P("Total Strength:"),
                        html.H4("—", id="total-strength", className="text-success"),
                        html.P("Average Strength:"),
                        html.H4("—", id="avg-strength", className="text-info"),
                        dbc.Button("Recalculate", color="primary", className="mt-2")
                    ])
                ])
            ], md=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Strength Distribution"),
                    dbc.CardBody([
                        dcc.Graph(
                            figure={"data": [], "layout": {"title": "Combined Strength Chart"}}
                        )
                    ])
                ])
            ], md=8),
        ]),
    ],
    fluid=True,
)
