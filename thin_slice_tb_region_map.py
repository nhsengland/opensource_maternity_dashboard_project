#https://geoportal.statistics.gov.uk/datasets/98493db82f5b4c3ba11538fc3a52199f_0/explore?location=52.030043%2C-3.448260%2C6.00
#https://geoportal.statistics.gov.uk/search?q=nhs%20region%202022
#https://www.ons.gov.uk/methodology/geography/geographicalproducts/digitalboundaries
#https://www.ons.gov.uk/methodology/geography/geographicalproducts/digitalboundaries

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors

def filter_for_total_babies(df, level):
    """
    Filter for TotalBabies, for a given level
    """
    #filter to level
    df_filtered = df[df["Org_Level"] == level]
    # filter to TotalBabies
    df_filtered = df_filtered[df_filtered["Dimension"] == "TotalBabies"]

    return df_filtered

def map_org_name(df):
    """
    Map the Names in the maternity df to the names in the geojson
    """
    name_mapping = {
    'LONDON COMMISSIONING REGION': 'London',
    'SOUTH WEST COMMISSIONING REGION': 'South West',
    'SOUTH EAST COMMISSIONING REGION': 'South East',
    'MIDLANDS COMMISSIONING REGION': 'Midlands',
    'EAST OF ENGLAND COMMISSIONING REGION': 'East of England',
    'NORTH WEST COMMISSIONING REGION': 'North West',
    'NORTH EAST AND YORKSHIRE COMMISSIONING REGION': 'North East and Yorkshire'}

    # Create the 'region_name' column by replacing the 'Org_Name' values
    df['region_name'] = df['Org_Name'].replace(name_mapping, regex=True)

    return df

def return_data_for_map():
    """
    Returns the df, fully processed and ready to create a map specifically for the TotalBabies metric for Regions
    """

    #read in csv and do pre-processing
    df = pd.read_csv("hosp-epis-stat-mat-msdscsv-2022-23.csv")
    df = filter_for_total_babies(df, "NHS England (Region)")
    df = map_org_name(df)

    # read in population excel and aggregate for regions
    df_pop = pd.read_excel("ons_2022-23_pop_health_geos.xlsx", sheet_name="Mid-2022 ICB 2023", header=3)
    df_pop_agg = df_pop.groupby(['NSHER 2023 Name', 'NHSER 2023 Code'])['Total'].sum().reset_index()

    #use ONS pop estimates as denominator for rate
    joined_df = df.merge(df_pop_agg, left_on="region_name", right_on="NSHER 2023 Name", how="left")
    joined_df['births per 1000'] = joined_df['Value'] / joined_df['Total'] * 1000


    # merge together geo data with rate data
    england = gpd.read_file("NHS_England_Regions_April_2021_EN_BUC_2022.geojson")
    joined_df = england.merge(joined_df, left_on="NHSER21NM", right_on="region_name")

    return joined_df

def create_plt_map(data):
    """
    Create the map using the given data, setting up colour scheme
    """
    nhs_colors = ['#B4D0FF', '#699EFF', '#1E6EFF', '#003087', '#001843']
    nhs_cmap = mcolors.LinearSegmentedColormap.from_list('NHS Blues', nhs_colors)
    fig, ax = plt.subplots(figsize=(10, 10))
    data.plot(ax=ax, column='births per 1000', cmap=nhs_cmap, edgecolor='black', legend=True)
    ax.set_axis_off()
    ax.set_title('Births per 1000 people: 2022-23', fontsize=16)
    plt.show()


# Run functions to create data and map
data = return_data_for_map()
#create_plt_map(data)
