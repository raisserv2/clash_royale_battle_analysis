import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

# Register this page as the landing page ('/')
dash.register_page(
    __name__,
    path='/',
    title='Battle Dashboard - Home',
    name='Home',
    order=0 
)

# --- Hero Section ---
hero_section = dbc.Row(
    [
        dbc.Col(
            [
                html.H1("Clash Royale Battle Analytics", className="display-3 fw-bold text-white"),
                html.P(
                    "Dive deep into card stats, compare troops, analyze deck archetypes, "
                    "and master the arena with data-driven insights.",
                    className="lead text-light",
                ),
                html.Hr(className="my-4 bg-light"),
                html.P(
                    "Select a tool below to get started.",
                    className="text-light"
                ),
                dbc.Button("Start Building Decks", color="primary", href="/builder", size="lg", className="mt-3 me-3"),
                dbc.Button("View Arena Stats", color="light", outline=True, href="/arena", size="lg", className="mt-3"),
            ],
            md=10, lg=8, className="py-5"
        )
    ],
    className="py-5 align-items-center justify-content-center text-center mb-5 hero-container"
)

# --- Feature Cards Helper function ---
def make_feature_card(title, description, link, icon="📊", color="primary"):
    return dbc.Card(
        [
            dbc.CardBody(
                [
                    html.H2(icon, className="display-4 mb-3"),
                    html.H4(title, className="card-title text-white"),
                    html.P(description, className="card-text text-muted"),
                    dbc.Button("Explore", color=color, outline=True, href=link, className="mt-auto stretched-link"),
                ],
                className="d-flex flex-column h-100 text-center"
            )
        ],
        className="h-100 shadow-sm hover-card border-light bg-dark",
        style={"minHeight": "250px"}
    )

# --- Features Grid ---
features_section = html.Div([
    dbc.Row(
        [
            html.H3("Analytics Tools", className="text-white mb-4 border-bottom border-primary pb-2 d-inline-block")
        ], 
        className="mb-3 text-center"
    ),
    dbc.Row(
        [
            dbc.Col(make_feature_card("Troop Comparison", "Head-to-head analysis of unit stats and interactions.", "/troop", "⚔️", "danger"), md=6, lg=4, className="mb-4"),
            dbc.Col(make_feature_card("Deck Builder", "Craft and optimize your ultimate battle deck.", "/builder", "🔨", "warning"), md=6, lg=4, className="mb-4"),
            dbc.Col(make_feature_card("Arena Stats", "Win rates and usage statistics across different arenas.", "/arena", "🏟️", "success"), md=6, lg=4, className="mb-4"),
            dbc.Col(make_feature_card("Evolution Impact", "Analyze how evolutions change card performance.", "/evo", "🧬", "info"), md=6, lg=3, className="mb-4"),
            dbc.Col(make_feature_card("Combo Synergy", "Discover powerful card combinations and win conditions.", "/combined", "🤝", "primary"), md=6, lg=3, className="mb-4"),
            dbc.Col(make_feature_card("Rarity Analysis", "Breakdown of performance by card rarity tiers.", "/rarity", "💎", "secondary"), md=6, lg=3, className="mb-4"),
            dbc.Col(make_feature_card("Archetypes", "Explore standard deck meta archetypes.", "/deck", "🃏", "light"), md=6, lg=3, className="mb-4"),
        ],
        className="justify-content-center"
    )
])

layout = dbc.Container(
    [
        hero_section,
        features_section,
        # Footer spacer
        html.Div(className="my-5")
    ],
    fluid=True,
    className="px-4"
)
