#!/usr/bin/env python3
"""
SpaceX Launch Prediction - Dash Dashboard
Interactive analytics platform for exploring SpaceX launch data
"""

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

# Initialize app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Sample data
data = {
    'LaunchSite': ['CCAFS SLC 40', 'CCAFS SLC 40', 'KSC LC 39A', 'VAFB SLC 4E'],
    'Orbit': ['LEO', 'GTO', 'GEO', 'Polar'],
    'Payload_mass__kg_': [4700, 8500, 6200, 3500],
    'class': [1, 1, 1, 0],
    'Date': ['2013-09-28', '2016-02-19', '2019-12-05', '2017-02-14']
}
df = pd.DataFrame(data)

# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("🚀 SpaceX Launch Analytics Dashboard", className="mt-4 mb-4")
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Label("Filter by Launch Site:"),
            dcc.Dropdown(
                id='site-dropdown',
                options=[{'label': 'All', 'value': 'all'}] + 
                        [{'label': site, 'value': site} for site in df['LaunchSite'].unique()],
                value='all'
            )
        ], width=6),
        dbc.Col([
            html.Label("Filter by Orbit:"),
            dcc.Dropdown(
                id='orbit-dropdown',
                options=[{'label': 'All', 'value': 'all'}] + 
                        [{'label': orbit, 'value': orbit} for orbit in df['Orbit'].unique()],
                value='all'
            )
        ], width=6),
    ], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='chart')
        ])
    ]),
    
], fluid=True)

@app.callback(
    Output('chart', 'figure'),
    [Input('site-dropdown', 'value'),
     Input('orbit-dropdown', 'value')]
)
def update_chart(selected_site, selected_orbit):
    filtered_df = df.copy()
    
    if selected_site != 'all':
        filtered_df = filtered_df[filtered_df['LaunchSite'] == selected_site]
    
    if selected_orbit != 'all':
        filtered_df = filtered_df[filtered_df['Orbit'] == selected_orbit]
    
    fig = px.bar(
        filtered_df.groupby('LaunchSite').size().reset_index(name='count'),
        x='LaunchSite',
        y='count',
        title='Number of Launches by Site'
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
