import thin_slice_tb_region_map as thin_slice_tb_region_map
import plotly.express as px

# Load DataFrame
df = thin_slice_tb_region_map.return_data_for_map()
# We need to switch to latitude-longitude, geopandas has a useful to_crs method for this
df = df.to_crs(epsg="4326")

# Create choropleth map
# For choropleth_mapbox geosjon can be a be a dataframe with a column called 'geometry' containing the area shapes.
# For this to work the index must match the column set as the `locations` argument.
# This is a bit odd as we have to supply the data twice with different arguments, so there's probably a neater
# way to do it!
geo = df[["region_name", "geometry"]].set_index("region_name")

# Define NHS colors
nhs_colors = ["#B4D0FF", "#699EFF", "#1E6EFF", "#003087", "#001843"]

fig = px.choropleth_mapbox(
    df,
    geojson=geo,
    locations="region_name",
    color="births per 1000",
    color_continuous_scale=nhs_colors,
    mapbox_style="carto-positron",
    center={"lat": 50, "lon": 0},
    zoom=5,
)
# Add title to the figure
fig.update_layout(title_text="Births per 1000 by Region")
# I think we should output to a specific folder, then we can ignore it with git.
fig.write_html("output/map.html")
