import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import networkx as nx
import pickle
import json
from collections import defaultdict
import ast
import dash
from dash import html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import json
import pandas as pd
from collections import defaultdict


dash.register_page(__name__, path="/evo", name="Evo Analysis")


def create_top_performers_dashboard(evo_df, non_evo_df, min_plays=100):

    """Dashboard showing top performers in different categories"""
    categories = [
        (
            "Top EVO Cards",
            evo_df[evo_df["total_plays"] >= min_plays].nlargest(
                10, "win_percentage"
            ),
        ),
        (
            "Top NON-EVO Cards",
            non_evo_df[non_evo_df["total_plays"] >= min_plays].nlargest(
                10, "win_percentage"
            ),
        ),
        ("Most Used EVO", evo_df.nlargest(10, "usage_count")),
        ("Most Used NON-EVO", non_evo_df.nlargest(10, "usage_count")),
    ]

    fig = make_subplots(rows=2, cols=2, subplot_titles=[cat[0] for cat in categories])

    for i, (title, data) in enumerate(categories):
        row = i // 2 + 1
        col = i % 2 + 1

        color = "#FF6B6B" if "EVO" in title else "#4ECDC4"

        fig.add_trace(
            go.Bar(
                x=data["win_percentage"],
                y=data["card"],
                orientation="h",
                marker_color=color,
                name=title,
                showlegend=False,
            ),
            row=row,
            col=col,
        )

    fig.update_layout(height=800, title_text="Top Performing Cards Dashboard")
    return fig

def create_evo_impact_analysis(evo_df, non_evo_df):

    """Analyze the impact of evolution on card performance"""
    # Get cards that have both EVO and NON-EVO versions
    all_cards = set(evo_df["card"]).union(set(non_evo_df["card"]))
    comparison_data = []

    for card in all_cards:
        evo_data = evo_df[evo_df["card"] == card]
        non_evo_data = non_evo_df[non_evo_df["card"] == card]

        if len(evo_data) > 0 and len(non_evo_data) > 0:
            evo_win = evo_data.iloc[0]["win_percentage"]
            non_evo_win = non_evo_data.iloc[0]["win_percentage"]
            win_rate_change = evo_win - non_evo_win

            comparison_data.append(
                {
                    "card": card,
                    "evo_win_rate": evo_win,
                    "non_evo_win_rate": non_evo_win,
                    "win_rate_change": win_rate_change,
                    "has_improvement": win_rate_change > 0,
                }
            )

    comparison_df = pd.DataFrame(comparison_data)

    fig = px.bar(
        comparison_df,
        x="card",
        y="win_rate_change",
        color="has_improvement",
        title="EVO Impact: Win Rate Change vs NON-EVO Version",
        labels={"win_rate_change": "Win Rate Change (%)", "card": "Card"},
        color_discrete_map={True: "#4ECDC4", False: "#FF6B6B"},
    )

    fig.update_layout(xaxis_tickangle=-45, showlegend=False)
    return fig

def create_evo_comparison_bubble(combined_df, min_plays=50):
    """Compare EVO vs NON-EVO performance"""
    df_filtered = combined_df[combined_df["total_plays"] >= min_plays]

    fig = px.scatter(
        df_filtered,
        x="usage_count",
        y="win_percentage",
        color="card_type",
        size="total_plays",
        hover_name="card",
        title="EVO vs NON-EVO Card Performance",
        labels={"usage_count": "Usage Count", "win_percentage": "Win Rate (%)"},
        color_discrete_map={"EVO": "#FF6B6B", "NON_EVO": "#4ECDC4"},
    )

    fig.update_layout(height=600)
    return fig

def create_comprehensive_evo_dashboard(evo_df, non_evo_df):
    """
    Shows EVO vs NON-EVO performance grouped by elixir cost.
    """
    
    # Initialize a standard figure instead of using make_subplots
    fig = go.Figure()

    # Add the EVO box plot trace
    fig.add_trace(
        go.Box(
            y=evo_df["win_percentage"],
            x=evo_df["elixir_cost"],
            name="EVO",
            marker_color="#FF6B6B",
        )
    )
    
    # Add the NON-EVO box plot trace
    fig.add_trace(
        go.Box(
            y=non_evo_df["win_percentage"],
            x=non_evo_df["elixir_cost"],
            name="NON-EVO",
            marker_color="#4ECDC4",
        )
    )
    
    # Update layout with a simpler title and settings
    fig.update_layout(
        height=500, 
        title_text="Performance by Elixir Cost (EVO vs NON-EVO)",
        xaxis_title="Elixir Cost",
        yaxis_title="Win Rate (%)",
        boxmode='group'  # Group the boxes side-by-side
    )

    return fig


card_db_path = "../#2 Data Storage/Visualization Data/card_database.csv"
battle_data_path = "../#2 Data Storage/Visualization Data/clash_royale_data_separated.pkl"

card_db = pd.read_csv(card_db_path)
print(f"✓ Loaded card database: {len( card_db)} cards")

# Load battle data
with open(battle_data_path, 'rb') as f:
    battle_data = pickle.load(f)

# Create DataFrames for EVO and NON-EVO
evo_df = pd.DataFrame({
    'card': list(battle_data['evo']['usage'].keys()),
    'usage_count': list(battle_data['evo']['usage'].values()),
    'win_count': [battle_data['evo']['wins'].get(card, 0) for card in battle_data['evo']['usage'].keys()],
    'total_plays': [battle_data['evo']['total_plays'].get(card, 0) for card in battle_data['evo']['usage'].keys()],
    'win_percentage': [battle_data['evo']['win_percentage'].get(card, 0) for card in battle_data['evo']['usage'].keys()],
    'card_type': 'EVO'
})

non_evo_df = pd.DataFrame({
    'card': list(battle_data['non_evo']['usage'].keys()),
    'usage_count': list(battle_data['non_evo']['usage'].values()),
    'win_count': [battle_data['non_evo']['wins'].get(card, 0) for card in battle_data['non_evo']['usage'].keys()],
    'total_plays': [battle_data['non_evo']['total_plays'].get(card, 0) for card in battle_data['non_evo']['usage'].keys()],
    'win_percentage': [battle_data['non_evo']['win_percentage'].get(card, 0) for card in battle_data['non_evo']['usage'].keys()],
    'card_type': 'NON_EVO'
})

# Merge with card database to get elixir cost and rarity
evo_df =  evo_df.merge(
     card_db[['englishName', 'elixir_cost', 'rarity', 'is_evo']], 
    left_on='card', right_on='englishName', how='left'
).drop('englishName', axis=1)

non_evo_df =  non_evo_df.merge(
     card_db[['englishName', 'elixir_cost', 'rarity', 'is_evo']], 
    left_on='card', right_on='englishName', how='left'
).drop('englishName', axis=1)

# Create combined DataFrame
combined_df = pd.concat([ evo_df,  non_evo_df], ignore_index=True)

print(f"✓ Loaded battle data: {len( combined_df)} card entries")
print(f"  - EVO cards: {len( evo_df)}")
print(f"  - NON-EVO cards: {len( non_evo_df)}")


fig_top_performers = create_top_performers_dashboard(evo_df, non_evo_df)
fig_impact_analysis = create_evo_impact_analysis(evo_df, non_evo_df)
fig_comparison_bubble = create_evo_comparison_bubble(combined_df)
fig_comprehensive = create_comprehensive_evo_dashboard(evo_df, non_evo_df)

layout = dbc.Container(
            [
                dbc.Row(
                    dbc.Col(html.H1("Clash Royale Evolution Analysis", className="text-center my-4"), width=12)
                ),
                dbc.Row(
                    dbc.Col(dcc.Graph(id="top-performers", figure=fig_top_performers), width=12),
                    className="mb-4"
                ),
                dbc.Row(
                    dbc.Col(dcc.Graph(id="impact-analysis", figure=fig_impact_analysis), width=12),
                    className="mb-4"
                ),
                dbc.Row(
                    dbc.Col(dcc.Graph(id="comparison-bubble", figure=fig_comparison_bubble), width=12),
                    className="mb-4"
                ),
                dbc.Row(
                    dbc.Col(dcc.Graph(id="comprehensive-dashboard", figure=fig_comprehensive), width=12),
                    className="mb-4"
                ),
            ],
            fluid=True,
        )










