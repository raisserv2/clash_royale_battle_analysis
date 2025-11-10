# pages/deck_archetypes.py
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import pickle
from typing import Dict, List, Optional # Keep for type hints

dash.register_page(__name__, path="/deck", name="Deck Archetypes")

# --- Data Preparation & Constants ---

# Default archetype mapping, can be overridden by passing a custom dict
DEFAULT_ARCHETYPE_MAPPING = {
    'Beatdown': ['Golem', 'Lava Hound', 'Giant', 'Electro Giant', 'Royal Giant'],
    'Control': ['X-Bow', 'Mortar', 'Tesla', 'Bomb Tower', 'Inferno Tower'],
    'Cycle': ['Hog Rider', 'Miner', 'Wall Breakers', 'Skeletons', 'Ice Spirit'],
    'Spell Bait': ['Goblin Barrel', 'Princess', 'Dart Goblin', 'Goblin Gang'],
    'Bridge Spam': ['Bandit', 'Royal Ghost', 'Battle Ram', 'Dark Prince'],
    'Siege': ['X-Bow', 'Mortar', 'Bomb Tower'],
    'Spawner': ['Goblin Hut', 'Furnace', 'Barbarian Hut', 'Tombstone']
}


def prepare_archetype_data(df: pd.DataFrame, mapping: Dict = DEFAULT_ARCHETYPE_MAPPING) -> pd.DataFrame:
    """
    Assigns archetypes to cards in the DataFrame based on a mapping.
    This is still used by the Treemap.
    """
    df_out = df.copy()
    df_out['archetype'] = 'Utility'  # Default value
    for archetype, cards in mapping.items():
        mask = df_out['card'].isin(cards)
        df_out.loc[mask, 'archetype'] = archetype # Note: This overwrites, which is a limitation for the treemap
    return df_out

# --- Visualization Functions ---

# 7. Deck Archetype Sunburst Chart
def create_archetype_sunburst(df: pd.DataFrame) -> go.Figure:
    """
    Sunburst chart of archetypes and cards.
    """
    sunburst_data = []
    
    sunburst_data.append({
        'ids': 'All Archetypes',
        'labels': 'All Archetypes',
        'parents': '',
        'values': 0.0, 
        'win_rate': 50.0 
    })

    for archetype, cards_list in DEFAULT_ARCHETYPE_MAPPING.items():
        archetype_cards = df[df['card'].isin(cards_list)]
        
        if not archetype_cards.empty:
            total_usage = archetype_cards['usage_count'].sum()
            avg_win_rate = (archetype_cards['win_percentage'] * archetype_cards['total_plays']).sum() / archetype_cards['total_plays'].sum()
            
            sunburst_data.append({
                'ids': archetype,
                'labels': archetype,
                'parents': 'All Archetypes', 
                'values': total_usage,
                'win_rate': avg_win_rate
            })
            
            for _, card in archetype_cards.iterrows():
                sunburst_data.append({
                    'ids': f"{archetype}-{card['card']}", 
                    'labels': card['card'],
                    'parents': archetype, 
                    'values': card['usage_count'],
                    'win_rate': card['win_percentage']
                })
    
    df_sunburst = pd.DataFrame(sunburst_data)
    
    df_sunburst_fig = df_sunburst[df_sunburst['parents'] != '']
    
    fig = px.sunburst(df_sunburst_fig, path=['parents', 'labels'], values='values',
                      color='win_rate', 
                      # --- COLOR CHANGE HERE ---
                      color_continuous_scale='turbo_r',
                    #   color_continuous_midpoint=50,      # Center the scale at 50%
                      title='Deck Archetype Hierarchy and Performance',
                      hover_data={'win_rate': ':.1f%'})
    
    fig.update_layout(
        height=800, 
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="'Clash Regular', Arial, sans-serif", size=14, color="#FFFFFF"),
        title_font=dict(family="'Clash Bold', Arial, sans-serif", size=20)
    )
    fig.update_traces(
        textfont=dict(family="'Clash Regular', Arial, sans-serif", color="#FFFFFF"),
        insidetextorientation='radial'
    )
    return fig

# 12. Card Performance Treemap
def create_card_treemap(df: pd.DataFrame, min_plays: int = 30) -> go.Figure:
    """
    Treemap showing card performance.
    Requires 'archetype' column (run prepare_archetype_data first).
    """
    if 'archetype' not in df.columns:
        print("Warning: 'archetype' column not found. Run prepare_archetype_data() first.")
        return go.Figure()
        
    df_filtered = df[df['total_plays'] >= min_plays]
    
    fig = px.treemap(df_filtered, path=['rarity', 'archetype', 'card'],
                     values='usage_count', color='win_percentage',
                     # --- COLOR CHANGE HERE ---
                     color_continuous_scale='turbo_r',
                     color_continuous_midpoint=50,      # Center the scale at 50%
                     title='Card Performance Treemap (Size=Usage, Color=Win Rate)')
    
    fig.update_layout(
        margin=dict(t=50, l=25, r=25, b=25),
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="'Clash Regular', Arial, sans-serif", size=14, color="#FFFFFF"),
        title_font=dict(family="'Clash Bold', Arial, sans-serif", size=20)
    )
    fig.update_traces(
        textfont=dict(family="'Clash Regular', Arial, sans-serif")
    )
    return fig


# --- Example Usage ---

def load_example_data(card_db_path='card_database.csv', battle_data_path='clash_royale_data_separated.pkl') -> Optional[pd.DataFrame]:
    """
    Loads and merges the example data for visualization.
    """
    print("🚀 Loading example data...")
    
    try:
        # Load card database
        card_db = pd.read_csv(card_db_path)
        
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
        
        # Merge with card database
        evo_df = evo_df.merge(
            card_db[['englishName', 'elixir_cost', 'rarity', 'is_evo']], 
            left_on='card', right_on='englishName', how='left'
        ).drop('englishName', axis=1)
        
        non_evo_df = non_evo_df.merge(
            card_db[['englishName', 'elixir_cost', 'rarity', 'is_evo']], 
            left_on='card', right_on='englishName', how='left'
        ).drop('englishName', axis=1)
        
        # Create combined DataFrame
        combined_df = pd.concat([evo_df, non_evo_df], ignore_index=True)

        # Prepare archetype data (still needed for the treemap)
        combined_df = prepare_archetype_data(combined_df, DEFAULT_ARCHETYPE_MAPPING)

        print("✓ Deck Archetype data loaded successfully.")
        return combined_df
        
    except Exception as e:
        print(f"❌ Error loading data for Deck page: {e}")
        return None


# 1. Load and prepare data
# (Assuming paths are relative to app.py in the root folder)
card_db_path = "../#2 Data Storage/Visualization Data/card_database.csv"
battle_data_path = "../#2 Data Storage/Visualization Data/clash_royale_data_separated.pkl"

df = load_example_data(card_db_path, battle_data_path)

# 2. Create Layout
if df is not None:
    # 2. Create visualizations
    Archetype_Sunburst = create_archetype_sunburst(df)
    Card_Treemap = create_card_treemap(df)

    # --- MODIFIED: Updated Layout ---
    layout = dbc.Container(
        [
            html.Div(
                [
                    html.H2("Deck Archetypes Visualization")
                ],
                className="page-title-container"
            ),
            
            # --- MODIFICATION: Wrapped in Card ---
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card([
                            dbc.CardHeader("Deck Archetype Hierarchy and Performance"),
                            dbc.CardBody([
                                dcc.Graph(figure=Archetype_Sunburst)
                            ])
                        ]),
                        width=12
                    )
                ],
                className="mb-4"
            ),
            
            # --- MODIFICATION: Wrapped in Card ---
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card([
                            dbc.CardHeader("Card Performance Treemap (Size=Usage, Color=Win Rate)"),
                            dbc.CardBody([
                                dcc.Graph(figure=Card_Treemap)
                            ])
                        ]),
                        width=12
                    )
                ]
            )
        ],
        fluid=True
    )
else:
    # Error layout
    layout = dbc.Container(
        [
            html.Div(
                html.H2("Deck Archetypes Visualization"),
                className="page-title-container"
            ),
            dbc.Alert(
                "Data could not be loaded. Please ensure 'card_database.csv' and 'clash_royale_data_separated.pkl' are present in the correct folder.",
                color="danger",
                className="mt-4"
            )
        ],
        fluid=True
    )