import pandas as pd
import sys
sys.path.append('./')
import config


def map_org_name(df):
    """
    Maps the organisational names in the 'Org_Name' column of the Maternity DataFrame
    to the corresponding region names based on a predefined mapping.

    Parameters:
    df (pandas.DataFrame): DataFrame containing the 'Org_Name' column with organisational names.

    Returns:
    pandas.DataFrame: DataFrame with an additional 'region_name' column where the organisational 
                      names have been mapped to region names.
    """
    # Dictionary to map organisational names to region names
    name_dict = {
        'LONDON COMMISSIONING REGION': 'London',
        'SOUTH WEST COMMISSIONING REGION': 'South West',
        'SOUTH EAST COMMISSIONING REGION': 'South East',
        'MIDLANDS COMMISSIONING REGION': 'Midlands',
        'EAST OF ENGLAND COMMISSIONING REGION': 'East of England',
        'NORTH WEST COMMISSIONING REGION': 'North West',
        'NORTH EAST AND YORKSHIRE COMMISSIONING REGION': 'North East and Yorkshire',
        'ALL SUBMITTERS': 'All Submitters'
    }

    # Create the 'region_name' column by replacing the 'Org_Name' values based on the mapping dictionary
    df['region_name'] = df['Org_Name'].replace(name_dict, regex=True)

    return df



def filter_for_measure_and_level(df, dimension, org_level):
    """
    Filters the input dataset for the given dimension and organisation level for the map.
    For example: dimension='SmokingStatusGroupBooking' and org_level='NHS England (Region)'.

    Parameters:
    df (pandas.DataFrame): DataFrame containing the data to be filtered.
    dimension (str): The dimension to filter by (e.g., 'SmokingStatusGroupBooking').
    org_level (str): The organisation level to filter by (e.g., 'NHS England (Region)').

    Returns:
    pandas.DataFrame: Filtered DataFrame containing only rows that match the specified dimension and organisation level.

    """
    # TODO: Implement error handling for invalid dimension or org_level values

    # Filter the DataFrame to only include rows with the specified organisation level and dimension

    df_filtered = df[df["Org_Level"] == org_level]


    df_filtered = df_filtered[df_filtered["Dimension"] == dimension]



    return df_filtered


def get_rates(df, dimension, measure_dict, org_level):
    """
    Calculates rates for a given dimension based on specified numerator and denominator
    measures, then returns the updated DataFrame with the calculated rates.

    Parameters:
    df (pandas.DataFrame): DataFrame containing the data to be processed.
    dimension (str): The dimension for which to calculate the rates.
    measure_dict (dict): Dictionary mapping dimensions to their corresponding numerator
                         and denominator measure names.

    Returns:
    pandas.DataFrame: DataFrame with the calculated rates for the specified dimension.
    """


    # Pivot the DataFrame to have 'Measure' values as columns and 'region_name' as the index
    df_pivoted = df.pivot(columns="Measure", values="Value", index="region_name")
    
    # Reset the index to convert 'region_name' from index to a column
    df_pivoted = df_pivoted.reset_index()

    
    # Calculate the rate by dividing the sum of the numerator by the sum of the denominator
    numerator_sum = df_pivoted[measure_dict[org_level][dimension]["numerator"]].sum(axis=1)

    denominator_sum = df_pivoted[measure_dict[org_level][dimension]["denominator"]].sum(axis=1)

    df_pivoted["Rate"] = numerator_sum / denominator_sum
    
    return df_pivoted


def join_pop_data(df):
    """
    Imports population data, aggregates it by region, and joins it onto the given DataFrame.
    This function is currently designed for calculating rates for total babies/deliveries.

    Parameters:
    df (pandas.DataFrame): DataFrame containing the data to be joined with the population data.
                           It must have a 'region_name' column.

    Returns:
    pandas.DataFrame: DataFrame resulting from the merge of the population data and the provided DataFrame,
                      with an additional 'Rate' column calculated using ONS population estimates as the denominator.
    """
    # Read the population data from the specified Excel file and sheet
    #This will need updated based on year!!!!!!!
    df_pop = pd.read_excel("data/ons_2022-23_pop_health_geos.xlsx", sheet_name="Mid-2022 ICB 2023", header=3)
    df_pop = df_pop[['NSHER 2023 Name', 'NHSER 2023 Code', 'Total']]

    # Aggregate the population data by region name and code, summing the total population and merge together
    df_pop_agg = df_pop.groupby(['NSHER 2023 Name', 'NHSER 2023 Code'])['Total'].sum().reset_index()
    joined_df = df.merge(df_pop_agg, left_on="region_name", right_on="NSHER 2023 Name", how="left")

    # Calculate the rate using the ONS population estimates as the denominator
    joined_df["Rate"] = joined_df['Value'] / joined_df['Total']
    
    return joined_df

def join_lat_lon_data(df):
    """
    Join the latitude and longitude data onto the main df, using the Org_Code
    """

    df_lat_lon = pd.read_csv("data/locations.csv")
    merged_df = pd.merge(df, df_lat_lon, left_on='Org_Code', right_on='org_code', how='left')

    return merged_df


def return_data_for_map(dimension, org_level, measure_dict, year):
    """
    Returns a DataFrame fully processed and ready to create a map.

    Parameters:
    dimension (str): The dimension for which to prepare the data (e.g., 'TotalBabies', 'TotalDeliveries').
    org_level (str): The organisation level to filter the data by (e.g., 'NHS England (Region)').
    measure_dict (dict): Dictionary mapping dimensions to their corresponding numerator and denominator
                         measure names for rate calculations from the config file

    Returns:
    geopandas.GeoDataFrame: A GeoDataFrame containing the processed data ready for map creation.
    """
    # Read the initial dataset from the CSV file, map names and filter
    df = pd.read_csv(config.data_source[year])
    df = map_org_name(df)
    df = join_lat_lon_data(df)

    df = filter_for_measure_and_level(df, dimension, org_level)
    
    # If the dimension is 'TotalBabies' or 'TotalDeliveries', join population data and calculate rates
    if dimension in config.special_dimensions:
        df_rates = join_pop_data(df)
        df_rates["Rate"] = df_rates["Rate"] * 1000
    else:
        # For other dimensions, calculate rates using the provided measure dictionary
        df_rates = get_rates(df, dimension, measure_dict, org_level)
        df_rates["Percent"] = df_rates["Rate"] * 100
        #merge the lat and lon back in
    
    
    df = df_rates.merge(df[['region_name', 'latitude', 'longitude']].drop_duplicates(), on='region_name', how='left', suffixes=('', '_'))
    #Enforce region order
    df = df.sort_values("region_name", key=lambda col:col.map(config.region_order), ignore_index=True)
    if org_level == "Provider":
        # I think the providers have changed so sorting doesn't make the numbers consistant
        # How could I do it without having a 200 line dictionary assigning values...
        df = df.sort_values("region_name")
    return df

def return_data_for_bar_chart(dimension, org_level, location, year):
    # Read the initial dataset from the CSV file, map names and filter     
    df = pd.read_csv(config.data_source[year])
    df = map_org_name(df)
    df = filter_for_measure_and_level(df, dimension, org_level)
    df = df[df["region_name"] == location]
    return df

def return_data_for_special_bar_chart(dimension, year):
    # This will return data to create a bar chart with Region on the X and Value/Rate on the Y
    # This is for TotalBabies/Deliveries

    df = pd.read_csv(config.data_source[year])
    df = map_org_name(df)
    df = filter_for_measure_and_level(df, dimension, "NHS England (Region)")
    df = join_pop_data(df)
    df["Rate"] = df["Rate"] * 1000

    return df


def merge_total_submitters(df_location, df_all_submitters, by_year=False):
    #Merges the two dataframes together and creates the percentage for the comparison marker to All Submitters
    if by_year:
        total_all_submitters = df_all_submitters['Value'].sum()
        df_all_submitters['Percentage'] = df_all_submitters['Value'] / total_all_submitters
        
        # Merge the percentage data with the location-specific data
        df_merged = pd.merge(df_location, df_all_submitters[['Measure', 'Percentage']], on='Measure', suffixes=('', '_all_submitters'))
        
        # Calculate the marker values
        df_merged['All Submitters Value'] = df_merged['Percentage'] * df_location['Value'].sum()

    else:
    # Calculate the total value for each measure in all submitters
        total_all_submitters = df_all_submitters['Value'].sum()
        df_all_submitters['Percentage'] = df_all_submitters['Value'] / total_all_submitters
        
        # Merge the percentage data with the location-specific data
        df_merged = pd.merge(df_location, df_all_submitters[['Measure', 'Percentage']], on='Measure', suffixes=('', '_all_submitters'))
        
        # Calculate the marker values
        df_merged['All Submitters Value'] = df_merged['Percentage'] * df_location['Value'].sum()

    return df_merged
    

def return_data_for_time_series(dimension, org_level, location):
    # Initialize an empty list to hold DataFrames
    all_data = []

    # Iterate over all years in the config
    for year in config.data_source.keys():
        # Read the dataset for the current year
        df = pd.read_csv(config.data_source[year])
        # Add the year column
        df['year'] = year
        # Append the DataFrame to the list
        all_data.append(df)
    
    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Map organization names
    combined_df = map_org_name(combined_df)
    
    # Filter for the specified measure and organization level
    combined_df = filter_for_measure_and_level(combined_df, dimension, org_level)

    print(combined_df)
    
    # Filter for the specified location
    if dimension not in config.special_dimensions:
        combined_df = combined_df[combined_df["region_name"] == location]
    
    return combined_df

def return_data_for_special_time_series(dimension, org_level):
    # Initialize an empty list to hold DataFrames
    all_data = []

    # Iterate over all years in the config
    for year in config.data_source.keys():
        # Read the dataset for the current year
        df = pd.read_csv(config.data_source[year])
        # Add the year column
        df['year'] = year
        # Append the DataFrame to the list
        all_data.append(df)

    # Concatenate all DataFrames into a single DataFrame
    combined_df = pd.concat(all_data, ignore_index=True)
    
    # Map organization names
    combined_df = map_org_name(combined_df)

    combined_df = filter_for_measure_and_level(combined_df, dimension, org_level)


    return combined_df
    