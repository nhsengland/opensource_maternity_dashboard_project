import process_data
import plotly.express as px

# Set variables:
# can this be done in a config file? in a dictionary?
org_level =  "NHS England (Region)"
rate_col = "Rate %"

dimension = "SmokingStatusGroupBooking"
numerator = "Smoker"
map_title = "Percentage of Smokers at Booking"

dimension = "SkinToSkinContact1HourTerm"
numerator = "Yes"
map_title = "Percentage of mothers that had skin to skin contact within 1 hour of birth"

dimension = "GestationLengthBirthGroup37"
numerator = ">=37 weeks"
map_title = "Percentage of Babies with a gestional length of 37 of more weeks (full term)"

dimension = "ComplexSocialFactorsInd"
numerator = "Y"
map_title = "Percentage of Mothers with Complex Social Factors Indicator " #what does this mean? site isnt loading: https://data.england.nhs.uk/ncdr/data_element/complex-social-factors-indicator/

dimension = "BirthweightTermGroup2500"
numerator = "2500g and over"
map_title = "Percentage of Babies with a birth weight of over 2500g"

dimension = "BabyFirstFeedBreastMilkStatus"
numerator = "Maternal or Donor Breast Milk"
map_title = "Percentage of Babies Fed Breast Milk (Maternal or Donor) as a first feed"

dimension = "ApgarScore5TermGroup7"
numerator = "7 to 10"
map_title = "Percentage of Babies with an APGAR Score or 7-10" #APGAR is quick test for healthy infant

dimension = "FolicAcidSupplement"
numerator = "numerator"
map_title = "Percentage of Mothers taking Folic Acid"


"""
rate_col = "Rate"
dimension = "TotalBabies"
numerator = ""
map_title = "Rate of births per 1000 people"

dimension = "TotalDeliveries"
numerator = ""
map_title = "Rate of deliveries per 1000 people"
"""

# Get map data
df = process_data.return_data_for_map(dimension, org_level, numerator)
# We need to switch to latitude-longitude, geopandas has a useful to_crs method for this
df = df.to_crs(epsg='4326')

# Create choropleth map
# For choropleth_mapbox geosjon can be a be a dataframe with a column called 'geometry' containing the area shapes.
# For this to work the index must match the column set as the `locations` argument.
# This is a bit odd as we have to supply the data twice with different arguments, so there's probably a neater
# way to do it!
geo = df[["region_name", "geometry"]].set_index("region_name")

# Define NHS colors
nhs_colors = ['#B4D0FF', '#699EFF', '#1E6EFF', '#003087', '#001843']

fig = px.choropleth_mapbox(df, 
                            geojson=geo, 
                            locations="region_name", 
                            color= rate_col,
                            color_continuous_scale=nhs_colors,
                            mapbox_style="carto-positron",
                            center={"lat": 50, "lon": 0},
                            zoom=5)
# Add title to the figure
fig.update_layout(title_text=map_title)
fig.write_html("output/map.html")