import thin_slice_tb_region_map
import plotly.express as px
import dash
from dash import dcc, html
import pandas as pd
import json

# Create choropleth map

# Load DataFrame
df = thin_slice_tb_region_map.return_data_for_map()

# Load GeoJSON file
with open('NHS_England_Regions_April_2021_EN_BUC_2022.geojson', 'r') as f:
    geojson_data = json.load(f)
df = df.to_crs(epsg='4326')


# Create choropleth map
fig = px.choropleth_mapbox(df, 
                            geojson=df.geometry, 
                            locations="region_name", 
                            #featureidkey="properties.NHSER21NM",
                            color='births per 1000',
                            mapbox_style="carto-positron",
                            center={"lat": 50, "lon": 0},
                            zoom=5)

fig.write_html("map.html")