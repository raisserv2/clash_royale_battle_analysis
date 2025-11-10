# pages/player_comparison.py
import dash
import pandas as pd
from dash import html, dcc, Input, Output, NoUpdate
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate


dash.register_page(__name__, path="/troop", name="Troop Comparison")

TROOP_PATH = "../#2 Data Storage/Utils/troop_name.csv"
TROOP_STATS_PATH = (
    "../#2 Data Storage/Data Visualization Data/clash_royale_card_stats.csv"
)
df_troops_stats = pd.read_csv(TROOP_STATS_PATH)
df_troops_name = pd.read_csv(TROOP_PATH)["Troop_name"]
         
layout = dbc.Container(
    [
        html.H2("Troop A vs Troop B"),
        html.Hr(),
        # Troop Comparison Section
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader("Troop Comparison"),
                                dbc.CardBody(
                                    [
                                        html.Label("Select Troop:"),
                                        dcc.Dropdown(
                                            id="troop-dropdown-1",
                                            options=[
                                                {"label": troop, "value": troop}
                                                for troop in df_troops_name
                                            ],
                                            placeholder="Select a troop...",
                                            searchable=True,
                                            clearable=True,
                                        ),
                                        html.Br(),
                                        html.Label("Evolution:"),
                                        dcc.RadioItems(
                                            id="evolution-selector-1",
                                            options=[
                                                {"label": "Normal", "value": "normal"},
                                                {"label": "Evolution", "value": "evo"},
                                            ],
                                            value="normal",
                                            inline=True,
                                        ),
    
                                        html.Hr(),
                                        html.Div(id="troop-info-1", className="mt-3"),
                                    ]
                                ),
                            ]
                        )
                    ],
                    md=6,
                ),
                dbc.Col(
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader("Troop Comparison"),
                                dbc.CardBody(
                                    [
                                        html.Label("Select Troop:"),
                                        dcc.Dropdown(
                                            id="troop-dropdown-2",
                                            options=[
                                                {"label": troop, "value": troop}
                                                for troop in df_troops_name
                                            ],
                                            placeholder="Select a troop...",
                                            searchable=True,
                                            clearable=True,
                                        ),
                                        html.Br(),
                                        html.Label("Evolution:"),
                                        dcc.RadioItems(
                                            id="evolution-selector-2",
                                            options=[
                                                {"label": "Normal", "value": "normal"},
                                                {"label": "Evolution", "value": "evo"},
                                            ],
                                            value="normal",
                                            inline=True,
                                        ),
                                        html.Hr(),
                                        html.Div(id="troop-info-2", className="mt-3"),
                                    ]
                                ),
                            ]
                        )
                    ],
                    md=6,
                ),
            ]
        ),
    ],
    fluid=True,
)

@dash.callback(
    Output("troop-info-1", "children"),
    Output("troop-info-2", "children"),
    Input("troop-dropdown-1", "value"),
    Input("evolution-selector-1", "value"),
    Input("troop-dropdown-2", "value"),
    Input("evolution-selector-2", "value"),
)
def update_troop_cards(troop1, evo1, troop2, evo2):
    def render_troop_card(selected_troop, evo_type):
        if not selected_troop:
            return html.I("Select a troop to view details.")

        troop_data = df_troops_stats[df_troops_stats["card"] == selected_troop]

        if troop_data.empty:
            return html.I("No data found for this troop configuration.")

        troop_data = troop_data.iloc[0].to_dict()

        # Try to render troop image
        img_component = None
        if "card" in troop_data and pd.notna(troop_data["card"]):
            img_path = f"../assets/2_icon_scrpaing/card_icons/{troop_data['card']}.webp"
            
            img_component = html.Img(
                id=f"img-{selected_troop}-{evo_type}",
                src=img_path,
                style={
                    "width": "100%",
                    "maxHeight": "220px",
                    "objectFit": "contain",
                    "marginBottom": "10px",
                },
            )
            print(img_component)


        stat_items = [html.Li(f"{k}: {v}") for k, v in troop_data.items()]

        # Wrap content in dcc.Loading
        return dcc.Loading(
            children=img_component),dbc.Card(
                        [
                            dbc.CardHeader(f"{selected_troop} ({evo_type.capitalize()})"),
                            dbc.CardBody(html.Ul(stat_items)),
                        ]
                    ),

    # Return both troop cards
    return render_troop_card(troop1, evo1), render_troop_card(troop2, evo2)