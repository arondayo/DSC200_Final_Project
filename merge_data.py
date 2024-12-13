#Import pandas to merge the data
import pandas as pd

"""
This function merges all of the different data sources we have collected and cleaned into one dataframe. We use pandas 
to organize the data and merge it using inner joins on the zipcode column. It is then returned to main for outputting.
This function receives 4 data frames as arguments and merges them into one. 
"""

def merge_data(df1, df2, df3, df4):
    #Merge the data using inner joins on zipcode column
    merged_data = pd.merge(df1, df2, how='inner', on="zipcode")
    merged_data = pd.merge(merged_data, df3, how='inner', on="zipcode")
    merged_data = pd.merge(merged_data, df4, how='inner', on="zipcode")

    #return the merged dataframe
    return merged_data


