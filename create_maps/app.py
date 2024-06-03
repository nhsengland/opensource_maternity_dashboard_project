from dash import Dash, dcc, html, Input, Output, callback
import json
import process_data
import plotly.express as px
import sys
import geopandas as gpd
sys.path.append('./')
import config


app = Dash(__name__)
org_level =  "NHS England (Region)"
dimension = "AgeAtBookingMotherGroup"

def get_map(org_level, dimension):
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
                                center={"lat": 53, "lon": 0},
                                zoom=5)


    fig.update_layout(title_text=config.measure_dict[dimension]["map_title"])
    fig.update_layout(clickmode='event+select')
    return fig

def get_bar_chart(org_level, dimension, location):
    df = process_data.return_data_for_bar_chart(dimension, org_level, location)
    fig = px.bar(df, x= "Measure", y="Value", title=location)
    return fig

app.layout = html.Div([
    dcc.Dropdown(list(config.measure_dict.keys()), dimension, id='dimension-dropdown'),
    dcc.Graph(
        id='map',
        figure=get_map(org_level, dimension)
    ),
    dcc.Graph(
        id='bar-chart',
        figure=get_bar_chart(org_level, dimension, location="London")
    )
    ])


@callback(
    Output('bar-chart', 'figure'),
    Input('dimension-dropdown', 'value'),
    Input('map', 'clickData'))
def display_bar_chart(dimension, clickData):
    if clickData is None:
        location = "All Submitters"
        org_level = "National"
    else:
        location = clickData["points"][0]["location"]
        org_level = "NHS England (Region)"
    fig = get_bar_chart(org_level, dimension, location)
    return fig


@callback(
    Output('map', 'figure'),
    Input('dimension-dropdown', 'value'))
def display_map(dimension):
    fig = get_map(org_level, dimension)
    return fig

if __name__ == '__main__':
    app.run(debug=True)
