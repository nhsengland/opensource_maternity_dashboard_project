import pandas as pd
import matplotlib.pyplot as plt

#import data
df = pd.read_csv("hosp-epis-stat-mat-msdscsv-2022-23.csv")

#get columns
columns = print(df.columns)

# removed the columns that'll have too much variety like Value/Org Name
cols = ['Period', 'Dimension', 'Org_Level', 'Measure',
       'Count_Of']
# for each column, print out each of the unique possible values
for col in cols:
    print(df[col].unique())