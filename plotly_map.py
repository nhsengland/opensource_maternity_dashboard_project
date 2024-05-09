import thin_slice_tb_region_map
import plotly.express as px

# Create choropleth map

# Load DataFrame
df = thin_slice_tb_region_map.return_data_for_map()
df = df.to_crs(epsg='4326')

# Create choropleth map
geo = df[["region_name", "geometry"]].set_index("region_name")
fig = px.choropleth_mapbox(df, 
                            geojson=geo, 
                            locations="region_name", 
                            color='births per 1000',
                            mapbox_style="carto-positron",
                            center={"lat": 50, "lon": 0},
                            zoom=5)

fig.write_html("output/map.html")