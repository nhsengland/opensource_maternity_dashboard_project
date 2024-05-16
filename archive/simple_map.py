# think about a map next: graph object (go - finer control)
#Choroplethmapbox
#https://geoportal.statistics.gov.uk/datasets/98493db82f5b4c3ba11538fc3a52199f_0/explore?location=52.030043%2C-3.448260%2C6.00
#https://geoportal.statistics.gov.uk/search?q=nhs%20region%202022
#https://www.ons.gov.uk/methodology/geography/geographicalproducts/digitalboundaries
#https://www.ons.gov.uk/methodology/geography/geographicalproducts/digitalboundaries

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame({"region_name": ["London","South East","South West","East of England","Midlands","North East and Yorkshire","North West"],
    "number": [1,2,3,4,5,6,7]})


england = gpd.read_file("NHS_England_Regions_April_2021_EN_BUC_2022.geojson")
merged = england.merge(df, left_on="NHSER21NM", right_on="region_name")
fig, ax = plt.subplots(figsize=(10, 10))

# Plot the data with different colors based on a column in the DataFrame
merged.plot(ax=ax, column='number', cmap='viridis', edgecolor='black', legend=True)
ax.set_axis_off()
ax.set_title('Map of England', fontsize=16)
plt.show()