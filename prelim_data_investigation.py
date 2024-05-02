import pandas as pd
import matplotlib.pyplot as plt

#import data
df = pd.read_csv("hosp-epis-stat-mat-msdscsv-2022-23.csv")

def create_bar_chart(dimension):
    """
    Create a bar chart for each dimension to figure out what the data looks like.
    Caveat: just using the national data for now
    """
    # filter to national
    df_national = df[df["Org_Level"] == "National"]
    
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
    plt.title(dimension + " at National level")
    plt.ylabel("Count for 2022-23 year")
    
    # Adjust the bottom margin to prevent labels from being cut off
    plt.subplots_adjust(bottom=0.5)
    
    # Save the chart
    plt.savefig(f"prelim_charts/{dimension}", bbox_inches='tight')
    plt.close()


# Replace missing values in "Measure" with values from "Dimension" - This is just for Total where there is no measure for Total
df['Measure'] = df['Measure'].fillna(df['Dimension'].map(str))

# Create bar charts for each Dimension
for dimension in df["Dimension"].unique():
    create_bar_chart(dimension)