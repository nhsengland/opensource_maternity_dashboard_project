import pandas as pd
import matplotlib.pyplot as plt
import os
import textwrap

def create_bar_chart(dimension, org_name):
    """
    Create a bar chart for each dimension to figure out what the data looks like.
    Caveat: just using the national data for now
    """
    # filter to national
    df_national = df[df["Org_Name"] == org_name]
    
    # filter to just the dimension we want
    df_filtered = df_national[df_national["Dimension"] == dimension]
    
    # Create the bar plot
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.bar(range(len(df_filtered)), df_filtered["Value"])
    
    # Wrap labels at spaces
    labels = df_filtered["Measure"].tolist()
    label_lines = ['\n'.join(l.split()) for l in labels]
    
    # Set tick locations and labels
    ax.set_xticks(range(len(df_filtered)))
    ax.set_xticklabels(label_lines, rotation=0, ha='center')
    
    # Set chart title and y-axis label
    plt.title(dimension + f" for {org_name}")
    plt.ylabel("Count for 2022-23 year")
    
    # Adjust the bottom margin to prevent labels from being cut off
    plt.subplots_adjust(bottom=0.5)
    
    # Create the folder path
    folder_path = os.path.join('prelim_charts', org_name)
    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)
    # Save the figure
    plt.savefig(os.path.join(folder_path, f"{dimension}.png"), bbox_inches='tight')
    plt.close()

df = pd.read_csv("hosp-epis-stat-mat-msdscsv-2022-23.csv")
# Replace missing values in "Measure" with values from "Dimension" - This is just for Total where there is no measure for Total
df['Measure'] = df['Measure'].fillna(df['Dimension'].map(str))

"""
# Create bar charts for each Dimension
# Run this to recreate charts for ALL orgs.
# Will take at least 10 minutes
for org in df["Org_Name"].unique():
    for dimension in df["Dimension"].unique():
        create_bar_chart(dimension, org)
"""

# chart of totalbabies/totaldeliveries for each region/provider in one chart
def create_chart_total_across_level(df, level, dimension):

# Filter the DataFrame to include only rows where Dimension matches the specified dimension
    filtered_df = df[df['Dimension'] == dimension]
    filtered_df = filtered_df[filtered_df['Org_Level'] == level]

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create the bar chart
    bars = ax.bar(range(len(filtered_df)), filtered_df["Value"], color="lightblue")

    # Add labels and title
    ax.set_ylabel("Value")
    ax.set_title(f"{dimension} by Organisation ({level})")

    # Set the x-axis tick labels with multi-line organization names
    ax.set_xticks(range(len(filtered_df)))
    ax.set_xticklabels([textwrap.fill(org_name, 20) for org_name in filtered_df["Org_Name"]], rotation=45, ha="center")

    # Create the folder path
    folder_path = os.path.join('total_charts')

    # Create the folder if it doesn't exist
    os.makedirs(folder_path, exist_ok=True)

    # Save the figure
    plt.savefig(os.path.join(folder_path, f"{dimension}_{level}.png"), bbox_inches='tight')
    plt.show()
    plt.close()


create_chart_total_across_level(df, "NHS England (Region)", "TotalBabies")
create_chart_total_across_level(df, "NHS England (Region)", "TotalDeliveries")

# provider has too many labels to be able to read graph
create_chart_total_across_level(df, "Provider", "TotalBabies")
create_chart_total_across_level(df, "Provider", "TotalDeliveries")

#from 2021 census: SW has 5.7 million (2021 census) and London 8.8 million. 
#But from chart looks like london is having more than 2x the number of babies than SW. 

# What next? 
# Would be interested in finding the rate for each of the metrics.
# think about a map next: graph object (go - finer control)
#Choroplethmapbox
#geopandas 
#download geojson
#https://geoportal.statistics.gov.uk/datasets/98493db82f5b4c3ba11538fc3a52199f_0/explore?location=52.030043%2C-3.448260%2C6.00
#https://geoportal.statistics.gov.uk/search?q=nhs%20region%202022
#https://www.ons.gov.uk/methodology/geography/geographicalproducts/digitalboundaries
#https://www.ons.gov.uk/methodology/geography/geographicalproducts/digitalboundaries