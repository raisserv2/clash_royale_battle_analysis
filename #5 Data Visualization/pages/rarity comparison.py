# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from plotly.subplots import make_subplots
# import numpy as np
# import networkx as nx
# from sklearn.preprocessing import StandardScaler
# from sklearn.decomposition import PCA
# import pickle
# import json
# from collections import defaultdict
# import ast
# from typing import Dict, List, Optional
# import pickle
# import json
# from collections import defaultdict
# import ast
# import dash
# from dash import html, dcc, callback, Input, Output
# import dash_bootstrap_components as dbc
# import plotly.graph_objects as go
# import json
# import pandas as pd
# from collections import defaultdict

# dash.register_page(__name__, path="/rarity", name="Rarity Analysis")

# # Custom color map for rarities
# RARITY_COLORS = {
#     "Common": "blue",
#     "Rare": "orange",
#     "Epic": "purple",
#     "Legendary": "green",
#     "Champion": "red"
# }

# # 13. Rarity Performance Violin Plot
# def create_rarity_violin_plot(df: pd.DataFrame) -> go.Figure:
#     """Violin plot showing win rate distribution by rarity"""
#     fig = px.violin(df, x='rarity', y='win_percentage',
#                     color='rarity', box=True, points="all",
#                     title='Win Rate Distribution by Rarity',
#                     color_discrete_map=RARITY_COLORS)
    
#     return fig


# # 15. Rarity Meta Share Donut Chart
# def create_rarity_meta_share(df: pd.DataFrame) -> go.Figure:
#     """Donut chart showing rarity distribution in the meta"""
#     rarity_share = df.groupby('rarity')['usage_count'].sum().reset_index()
    
#     fig = px.pie(rarity_share, values='usage_count', names='rarity',
#                  title='Rarity Distribution in Current Meta (by Usage Count)',
#                  hole=0.4, color='rarity',
#                  color_discrete_map=RARITY_COLORS)
    
#     return fig

# # 1. Interactive Card Win Rate vs Usage Bubble Chart
# def create_win_rate_usage_bubble(df: pd.DataFrame, min_plays: int = 100) -> go.Figure:
#     """Win Rate vs Usage with Elixir Cost as bubble size and custom rarity colors"""
#     df_filtered = df[df['total_plays'] >= min_plays]
    
#     fig = px.scatter(
#         df_filtered,
#         x='usage_count',
#         y='win_percentage',
#         size='elixir_cost',
#         hover_name='card',
#         color='rarity',
#         size_max=30,
#         title='Card Performance: Win Rate vs Usage (Bubble Size = Elixir Cost)',
#         labels={'usage_count': 'Usage Count', 'win_percentage': 'Win Rate (%)'},
#         color_discrete_map=RARITY_COLORS
#     )
    
#     # Add average lines
#     avg_usage = df_filtered['usage_count'].mean()
#     avg_win = df_filtered['win_percentage'].mean()
    
#     fig.add_hline(y=avg_win, line_dash="dash", line_color="red")
#     fig.add_vline(x=avg_usage, line_dash="dash", line_color="red")
    
#     fig.update_layout(height=600, xaxis_type="log")
#     return fig



