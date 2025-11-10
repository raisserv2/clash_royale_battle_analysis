# pages/combined_strength.py
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

from dash import Output, Input
dash.register_page(__name__, path="/combined", name="Combined Strength")

INPUT_FILE = "../#2 Data Storage/Data Visualization Data/card_pair_data.csv"

def create_meta_map(csv_path):
    """
    Reads the card pair stats and generates an interactive
    scatter plot of Usage vs. Win Rate.
    """
    

    df=pd.read_csv(csv_path)
        
    df['pair_name'] = df['card_1'] + " + " + df['card_2']


    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df['usage_count'],
            y=df['win_rate_percent'],
            mode='markers',
            marker=dict(
                size=5,
                color=df['win_rate_percent'], # Color points by their win rate
                # --- COLORSCALE CHANGE HERE ---
                colorscale='Bluered'
                 ,  # Changed from 'RdYlGn' to 'Portland'
                # Other good options: 'Bluered', 'Spectral', 'Plasma'
                # Or a custom one: [[0, 'red'], [0.5, 'white'], [1, 'green']]
                # ------------------------------
                showscale=True,
                colorbar=dict(title='Win Rate %')
            ),
            hovertemplate=(
                f"<b>Pair:</b> %{{customdata[0]}}<br>"
                f"<b>Usage:</b> %{{x:,}}<br>"
                f"<b>Win Rate:</b> %{{y:.1f}}%"
                "<extra></extra>"
            ),
            customdata=df[['pair_name']]
        )
    )

    fig.add_hline(
        y=50.0,
        line_dash="dash",
        line_color="black",
        annotation_text="50% Win Rate",
        annotation_position="bottom right"
    )

    fig.update_layout(
        title="Card Pair Meta Map (Usage vs. Win Rate)",
        xaxis_title="Popularity (Usage Count)",
        yaxis_title="Effectiveness (Win Rate %)",
        xaxis_type="log",
        yaxis=dict(
            range=[35, 65]
        ),
        hovermode="closest",
        height=700,
        template='plotly_white'
    )
    return fig



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
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id="meta-map-graph",
                    figure=create_meta_map(INPUT_FILE) if create_meta_map(INPUT_FILE) else go.Figure(),
                    config={"displayModeBar": False}

                )
            ])
        ])
    ]),
   
    ] , fluid=True)

@dash.callback(
    Output("meta-map-graph", "figure"),
    Input("meta-map-graph", "id")  # Dummy input to trigger on page load
)
def update_meta_map(_):
    fig = create_meta_map(INPUT_FILE)
    if fig is None:
        # Return an empty figure if data is missing
        return go.Figure(layout={"title": "No data available"})
    return fig




    
