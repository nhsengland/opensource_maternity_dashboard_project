#https://geoportal.statistics.gov.uk/datasets/98493db82f5b4c3ba11538fc3a52199f_0/explore?location=52.030043%2C-3.448260%2C6.00
#https://geoportal.statistics.gov.uk/search?q=nhs%20region%202022
#https://www.ons.gov.uk/methodology/geography/geographicalproducts/digitalboundaries
#https://www.ons.gov.uk/methodology/geography/geographicalproducts/digitalboundaries

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as mcolors


def map_org_name(df):
    """
    Preprocessing:
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


def filter_for_measure_and_level(df, dimension, org_level):
    """
    FIlters input dataset for the give dimension and level for the map 
    E.g: Dimension = SmokingStatusGroupBooking and org_level= NHS England (Region)
    """
    #TODO: if level/dimension isn't valid-> error

    #filter to level
    df_filtered = df[df["Org_Level"] == org_level]

    # filter to given Dimension
    df_filtered = df_filtered[df_filtered["Dimension"] == dimension]

    return df_filtered


def get_rate_for_dimension(df, numerator):
    """
    From the numerator, get the relevant rate
    numerator will be whatever we are getting the rate of. E.g "Smoker". 
    """
    # eg for smokers we need to add up total datapoints, then divide to find rate
    # Filters out values for missing, and get a df with the total number of smokers/non smokrs
    filtered_df = df[~df['Measure'].str.contains('Missing')]
    result = filtered_df.groupby('Org_Name')['Value'].sum().reset_index()
    result.rename(columns={'Value': 'Total_Sum'}, inplace=True)

    # Get a df of justs smokers for each region and join on Org_Name
    # Filter rows where measure is "Smoker"
    smoker_df = df[df['Measure'] == numerator]

    #jin df together on Org_Name
    merged_df = smoker_df.merge(result, on="Org_Name")

    merged_df["Rate %"] = merged_df["Value"] / merged_df["Total_Sum"] * 100


    return merged_df


def join_geojson_data(df):
    """
    Join the geojson data onto the dataframe
    MUST have the region_name column matching the names in the geojson
    """
    geojson = gpd.read_file("data/NHS_England_Regions_April_2021_EN_BUC_2022.geojson")
    joined_df = geojson.merge(df, left_on="NHSER21NM", right_on="region_name")

    return joined_df

def join_pop_data(df):
    """
    Import the population data, aggregate it to region, and join onto df
    """
    # read in population excel and aggregate for regions
    df_pop = pd.read_excel("data/ons_2022-23_pop_health_geos.xlsx", sheet_name="Mid-2022 ICB 2023", header=3)
    df_pop_agg = df_pop.groupby(['NSHER 2023 Name', 'NHSER 2023 Code'])['Total'].sum().reset_index()

    
    joined_df = df.merge(df_pop_agg, left_on="region_name", right_on="NSHER 2023 Name", how="left")

    
    #use ONS pop estimates as denominator for rate
    #this code is specifically for this birth rate. 
    #joined_df['births per 1000'] = joined_df['Value'] / joined_df['Total'] * 1000

    return joined_df

def return_data_for_map(dimension, org_level, numerator):
    """
    Returns the df, fully processed and ready to create a map specifically for the TotalBabies metric for Regions
    """

    df = pd.read_csv("data/hosp-epis-stat-mat-msdscsv-2022-23.csv")
    df = map_org_name(df)
    df = filter_for_measure_and_level(df, dimension, org_level)
    df = get_rate_for_dimension(df, numerator) 
    map_df = join_geojson_data(df)

    return map_df
