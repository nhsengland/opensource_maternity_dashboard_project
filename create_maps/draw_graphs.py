
from create_maps import process_data
import plotly.express as px
import sys
import geopandas as gpd
import plotly.graph_objects as go
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
                                color=config.measure_dict["NHS England (Region)"][dimension]["rate_col"],
                                color_continuous_scale=nhs_colors,
                                mapbox_style="carto-positron",
                                center={"lat": 53, "lon": -2},
                                zoom=5.2,
                                custom_data=['region_name', config.measure_dict["NHS England (Region)"][dimension]["rate_col"]]
                                )
    
    if dimension in config.special_dimensions:
        hover_template = (
            '%{customdata[0]}<br>'
            '%{customdata[1]:.2f}<extra></extra>'
        )
    else:
        hover_template = (
            '%{customdata[0]}<br>'
            '%{customdata[1]:.2f}%<extra></extra>'
        )
        

    fig.update_traces(hovertemplate=hover_template)



    
    fig.update_layout(clickmode='event+select')

    fig.update_coloraxes(colorbar={'orientation':'h',
                                   'title': ""})
    fig.update_layout(coloraxis_colorbar_y=-0.1)

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
                                color=config.measure_dict["Provider"][dimension]["rate_col"],
                                color_continuous_scale=nhs_colors,
                                mapbox_style="carto-positron",
                                center={"lat": 53, "lon": -2},
                                zoom=5.5)
    
    percent_col = config.measure_dict["Provider"][dimension]["rate_col"]
    sign = "%" if percent_col == "Percent" else ""

    fig.add_trace(
        go.Scattermapbox(
            lat=df['latitude'],
            lon=df['longitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=20,
                color=df[percent_col],
                colorscale=nhs_colors,
                colorbar=dict(title='', orientation='h', y=-0.1)
            ),
            customdata=df[['region_name', percent_col]],
            hovertemplate='%{customdata[0]}<br>%{customdata[1]:.2f}' + sign + '<extra></extra>'
        )
    )

    fig.update_layout(clickmode='event+select')

    fig.update_coloraxes(colorbar={'orientation':'h', 'title': ""})
    fig.update_layout(coloraxis_colorbar_y=-0.1)

    if selectedpoints is not None:
        fig.update_traces(selectedpoints=selectedpoints)
        
    return fig

def draw_special_bar_chart(dimension, year):
    df = process_data.return_data_for_special_bar_chart(dimension, year)
    # Create the bar chart
    # Should this be the rate (reflection of map) or the raw numbers
    fig = px.bar(df, x="Org_Name", y="Rate")
    fig.update_layout(xaxis_title='', yaxis_title='')
   
    return fig


def draw_bar_chart(org_level, dimension, year, location):
    print("drawing bar chart")
    print(dimension, org_level, location, year)
    df_location = process_data.return_data_for_bar_chart(dimension, org_level, location, year)
    df_all_submitters = process_data.return_data_for_bar_chart(dimension, "National", "All Submitters", year)

    # Merge together the df with the All Submitters data to get marker data
    df_merged = process_data.merge_total_submitters(df_location, df_all_submitters)

    # Create the bar chart
    fig = px.bar(df_merged, x="Measure", y="Value")
    
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

    fig.update_layout(legend={"yanchor": "middle",
                              "xanchor": "left",
                              "y":0.98,
                              "x":0})
    fig.update_layout(xaxis_title='', yaxis_title='')


    return fig


def draw_time_series(org_level, dimension, location):
    df_location = process_data.return_data_for_time_series(dimension, org_level, location)

    # Strip the first characters to get numeric year for sorting
    df_location['numeric_year'] = df_location['year'].str.split('-').str[0].astype(int)

    # Sort by numeric year
    df_location = df_location.sort_values(by='numeric_year')

    if dimension in config.special_dimensions:
        split_on = "Org_Name"
    else:
        split_on = "Measure"

    # Create custom hover text
    df_location['hover_text'] = df_location.apply(
        lambda row: f"Year: {row['year']}<br>{split_on}: {row[split_on]}<br>Value: {row['Value']}", axis=1)
    
    # Create the time series line graph with custom hover text
    fig = px.line(df_location, x="year", y="Value", color=split_on,
                  hover_data={'hover_text': True})
    
    # Update hover data to use custom text
    fig.update_traces(hovertemplate='%{customdata}')
    
    # Add round, black dots at each point in the graph
    for measure in df_location[split_on].unique():
        df_measure = df_location[df_location[split_on] == measure]

        fig.add_trace(
            go.Scatter(
                x=df_measure['year'], 
                y=df_measure['Value'], 
                mode='markers',
                name=f'{measure} Dots',
                marker=dict(
                    symbol='circle',
                    size=6,
                    color='black'
                ),
                hoverinfo='skip',
                showlegend=False 
            )
        )

    fig.update_layout(xaxis_title='', yaxis_title='')

    return fig