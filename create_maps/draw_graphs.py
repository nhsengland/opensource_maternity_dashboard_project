
import process_data
import plotly.express as px
import sys
import geopandas as gpd
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import json
sys.path.append('./')
import config


def draw_region_map(org_level, dimension, year, selectedpoints=None):
    # Get map data in the correct format
    df = process_data.return_data_for_map(dimension, org_level, config.measure_dict, year)
    
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


    fig.update_layout(title_text=f'{config.measure_dict[dimension]["map_title"]} for {year}')
    fig.update_layout(clickmode='event+select')
    if selectedpoints is not None:
        fig.update_traces(selectedpoints=selectedpoints)

    return fig

def draw_provider_map(org_level, dimension, year, selectedpoints=None):
    # Get map data in the correct format
    df = process_data.return_data_for_map(dimension, org_level, config.measure_dict, year)
    
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


    if org_level == "Provider":
        df = process_data.return_data_for_map(dimension, "Provider", config.measure_dict, year)
        percent_col = config.measure_dict[dimension]["rate_col"]

        fig.add_trace(
            go.Scattermapbox(
                lat=df['latitude'],
                lon=df['longitude'],
                mode='markers',
                marker=go.scattermapbox.Marker(
                    size=20,
                    color = df['Percent'],
                    colorscale=nhs_colors                   
                ),
                text=df.apply(lambda row: f"{row['region_name']}<br>{row[percent_col]}%", axis=1),
                hoverinfo='text'
            )
        )

    fig.update_layout(title_text=f'{config.measure_dict[dimension]["map_title"]} for {year}')
    fig.update_layout(clickmode='event+select')
    if selectedpoints is not None:
        # update color here 
        fig.update_traces(selectedpoints=selectedpoints)
        
    return fig


def draw_special_bar_chart(dimension, year):
    df = process_data.return_data_for_special_bar_chart(dimension, year)
    # Create the bar chart
    # Should this be the rate (reflection of map) or the raw numbers
    fig = px.bar(df, x="Org_Name", y="Rate", title=f"{dimension}. Bar chart showing the rate of {dimension} per 1000 people for {year}")
    return fig

def draw_bar_chart(org_level, dimension, year, location):
    df_location = process_data.return_data_for_bar_chart(dimension, org_level, location, year)
    df_all_submitters = process_data.return_data_for_bar_chart(dimension, "National", "All Submitters", year)

    # Merge together the df with the All Submitters data to get marker data
    df_merged = process_data.merge_total_submitters(df_location, df_all_submitters)

    # Create the bar chart
    fig = px.bar(df_merged, x="Measure", y="Value", title=f"{location}: {dimension}. Bar chart of broken down data, with markers comparing to All Submitters for {year}")
    
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
    