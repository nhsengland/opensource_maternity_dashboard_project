import thin_slice_tb_region_map
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Load DataFrame
df = thin_slice_tb_region_map.return_data_for_map()
# We need to switch to latitude-longitude, geopandas has a useful to_crs method for this
df = df.to_crs(epsg="4326")

# Define NHS colors
nhs_colors = ["#B4D0FF", "#699EFF", "#1E6EFF", "#003087", "#001843"]

# Create choropleth map figure
geo = df[["region_name", "geometry"]].set_index("region_name")
fig = px.choropleth_mapbox(
    df,
    geojson=geo,
    locations="region_name",
    color="births per 1000",
    color_continuous_scale=nhs_colors,
    mapbox_style="carto-positron",
    center={"lat": 53, "lon": 0},
    zoom=5,
)

# Initialize Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div(
    [
        html.H1("Births per 1000 by Region"),
        dcc.Graph(id="map", figure=fig, style={"height": "100vh"}),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True)
