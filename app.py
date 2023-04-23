import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, dependencies

# 1 - Create some graph for RATP dataset

df = pd.read_csv('trafic-annuel-entrant-par-station-du-reseau-ferre-2021.csv', sep=';')
sorted_df = df.sort_values(by=['Trafic'], ascending=False)
topBar = sorted_df.head(10)
topPie = df.head(20)

# 2 - Create some graph for IDF dataset
df2 = pd.read_csv('emplacement-des-gares-idf.csv', sep=';')
exploit_counts = df2.groupby('exploitant')['nom'].count().reset_index()
ligne_counts = df2.groupby('ligne')['nom'].count().reset_index()


df2[['lat', 'lng']] = df2['Geo Point'].str.split(',', expand=True)
df2['lat'] = df2['lat'].str.strip().astype(float)
df2['lng'] = df2['lng'].str.strip().astype(float)


app = Dash(__name__)

app.layout = html.Div(children=[
    # Create a bar chart that represents the TOP 10 stations with the biggest trafic
    html.H1("1- Stations avec le plus de trafic", style={'background-color': '#51E9BF', 'color':'#05509A','text-align':'left'}),

    # 3 - Add some global filters
    # One filter for réseau (field from the RATP dataset)
    dcc.Dropdown(
        id='Réseau-filter',
        options=[{'label': category, 'value': category} for category in sorted_df['Réseau'].unique()],
        value=None,
        placeholder='Séléctionner un réseau'
    ),

    dcc.Graph(
            id='bar-chart',
            figure=px.bar(topBar, x='Station', y='Trafic'),
            style={'width': '50%', 'align': 'right', 'display': 'inline-block'}
    ),
    # Create a Pie chart that represents trafic per cities (to make it clear, you can take only the TOP 5)
    dcc.Graph(
            id='pie-chart',
            figure=px.pie(topPie, values='Trafic', names='Ville'),
            # Organize those two chart on the same row (they have to be side by side)
            style={'width': '50%', 'align': 'right', 'display': 'inline-block'}
    ),

    # Create a bar chart that represents the number of stations per exploitant
    html.H1("2- Nombre de station par lignes et par exploitants", style={'background-color': '#51E9BF', 'color':'#05509A',
                                                                      'text-align':'left'}),
    # One filter for exploitant (field from the IDF dataset)
    dcc.Dropdown(
        id='exploit-filter',
        options=[{'label': category, 'value': category} for category in df2['exploitant'].unique()],
        value=None,
        placeholder='Séléctionner un exploitant'
    ),

    dcc.Graph(
        id='bar-chart2',
        figure=px.bar(exploit_counts, x='exploitant', y='nom')
    ),

    # Create a chart that represents the number of stations per line
    dcc.Graph(
        id='bar-chart3',
        figure=px.bar(ligne_counts, x='ligne', y='nom',
                      labels={'Ligne': 'Ligne', 'nom': 'Nombre de station'}
                      )),

    # 4 - Create an interactive map
    html.H1("4- Map interactive", style={'background-color': '#51E9BF', 'color':'#05509A',
                                         'text-align':'left'}),
    dcc.Graph(id="map-graph", figure=px.scatter_mapbox(
        df2,
        lat='lat',
        lon='lng',
        hover_name='Geo Point',
        zoom=6
    ).update_layout(mapbox_style='open-street-map'))

])


@app.callback(
    dependencies.Output('bar-chart', 'figure'),
    dependencies.Input('Réseau-filter', 'value')
)
def update_bar_chart(category):
    if category is None:
        # Keep all categories if no value has been selected
        filtered_df = topBar
    else:
        # Filter the df based on selection
        filtered_df = topBar[topBar['Réseau'] == category]

    return px.bar(filtered_df, x='Station', y='Trafic')



@app.callback(
    dependencies.Output('bar-chart2', 'figure'),
    dependencies.Input('exploit-filter', 'value')
)
def update_bar_chart(category):
    if category is None:
        # Keep all categories if no value has been selected
        filtered_df = exploit_counts
    else:
        # Filter the df based on selection
        filtered_df = exploit_counts[exploit_counts['exploitant'] == category]

    return px.bar(filtered_df, x='exploitant', y='nom')


# Run the script.
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)
