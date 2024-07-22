import process_data
import plotly.express as px
import sys
import geopandas as gpd

sys.path.append("./")
import config

org_level = "NHS England (Region)"
for dimension in config.measure_dict:

    # Get map data in the correct format
    df = process_data.return_data_for_map(dimension, org_level, config.measure_dict)
    geo_df = geojson = gpd.read_file(
        "data/NHS_England_Regions_April_2021_EN_BUC_2022.geojson"
    )
    geo_df = geo_df.to_crs(epsg="4326")
    geo_df = geo_df[["NHSER21NM", "geometry"]].set_index("NHSER21NM")

    # Define NHS colours for map
    nhs_colors = ["#B4D0FF", "#699EFF", "#1E6EFF", "#003087", "#001843"]

    fig = px.choropleth_mapbox(
        df,
        geojson=geo_df,
        locations="region_name",
        color=config.measure_dict[dimension]["rate_col"],
        color_continuous_scale=nhs_colors,
        mapbox_style="carto-positron",
        center={"lat": 53, "lon": 0},
        zoom=5,
    )

    # Add title to the figure
    fig.update_layout(title_text=config.measure_dict[dimension]["map_title"])
    # output click events so that when clicked it updates other parts of map
    fig.write_html(f"output/{dimension}_map.html")
