from dash import Dash, dcc, html, Input, Output, callback
import process_data
import plotly.express as px
import sys
import geopandas as gpd
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import json
sys.path.append('./')
import config


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
org_level =  "NHS England (Region)"
dimension = "AgeAtBookingMotherGroup"

def get_map(org_level, dimension, selectedpoints=None):
    # Get map data in the correct format
    df = process_data.return_data_for_map(dimension, org_level, config.measure_dict)
    geo_df = gpd.read_file("data/NHS_England_Regions_April_2021_EN_BUC_2022.geojson")
    geo_df = geo_df.to_crs(epsg='4326')
    geo_df = geo_df[["NHSER21NM", "geometry"]].set_index("NHSER21NM")
    nhs_colors = ['#B4D0FF', '#699EFF', '#1E6EFF', '#003087', '#001843']

    fig = px.choropleth_mapbox(df, 
                                geojson=geo_df, 
                                locations="region_name", 
                                color=config.measure_dict[dimension]["rate_col"],
                                color_continuous_scale=nhs_colors,
                                mapbox_style="carto-positron",
                                center={"lat": 53, "lon": -2},
                                zoom=5.5)


    fig.update_layout(title_text=config.measure_dict[dimension]["map_title"])
    fig.update_layout(clickmode='event+select')
    if selectedpoints is not None:
        fig.update_traces(selectedpoints=selectedpoints)
    return fig

def get_bar_chart(org_level, dimension, location):
    df_location = process_data.return_data_for_bar_chart(dimension, org_level, location)
    df_all_submitters = process_data.return_data_for_bar_chart(dimension, "National", "All Submitters")

    # Merge together the df with the All Submitters data to get marker data
    df_merged = process_data.merge_total_submitters(df_location, df_all_submitters)

    # Create the bar chart
    fig = px.bar(df_merged, x="Measure", y="Value", title=f"{location}: {dimension}. Bar chart of broken down data, with markers comparing to All Submitters")
    
    # Add custom markers for All Submitters
    fig.add_trace(
        go.Scatter(
            x=df_merged['Measure'], 
            y=df_merged['All Submitters Value'], 
            mode='markers',
            name='All Submitters',
            marker=dict(
                symbol='cross',
                size=10,
                color='red'
            )
        )
    )
    
    return fig


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",  # Adjusted the width to reduce the gap
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "8rem", 
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout", className="lead"
        ),
        dcc.Dropdown(list(config.measure_dict.keys()), dimension, id='dimension-dropdown'),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(
    [dbc.Row(
        [
            dbc.Col(
                dcc.Graph(
                    id='map',
                    figure=get_map(org_level, dimension),
                    style={"height": "800px"}
                ), width=5, style={"padding": "0"}
            ),
            dbc.Col(
                dcc.Graph(
                    id='bar-chart',
                    figure=get_bar_chart(org_level, dimension, location="All Submitters"),
                    style={"height": "800px"}
                ), width=7, style={"padding": "0"} 
            )
        ]
    ),
            html.Div([
            html.Pre(id='click-data')
        ]),   

    html.Div([
            html.Pre(id='selectedpoints')
        ]),   
    ],
    style=CONTENT_STYLE
)

app.layout = html.Div([
    dcc.Location(id="url"),
    dbc.Row([
        dbc.Col(sidebar, width=1),
        dbc.Col(content, width=11, style={"padding": "0"})
    ]),
])


@callback(
    Output('click-data', 'children'),
    Input('map', 'selectedData'))
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)


# callback(
#     Output('selectedpoints', 'children'),
#     Input('map', 'selectedData'))
# def display_click_data(clickData):
#     return json.dumps(clickData, indent=2)


@callback(
    Output('bar-chart', 'figure'),
    Input('dimension-dropdown', 'value'),
    Input('map', 'selectedData'))
def display_bar_chart(dimension, selectedData):
    if selectedData is None:
        location = "All Submitters"
        org_level = "National"
    else:
        location = selectedData["points"][0]["location"]
        org_level = "NHS England (Region)"
    fig = get_bar_chart(org_level, dimension, location)
    return fig



@callback(
    Output('map', 'figure'),
    Output('selectedpoints', 'children'),
    Input('dimension-dropdown', 'value'),
    Input('map', 'selectedData'))
def display_map(dimension, selectedData):
    if selectedData is None:
        selectedpoints = None
    else:
        selectedpoints = [point["pointIndex"] for point in selectedData["points"]]
    fig = get_map(org_level, dimension, selectedpoints=selectedpoints)
    return fig, json.dumps(selectedpoints)

if __name__ == '__main__':
    app.run(debug=True)
