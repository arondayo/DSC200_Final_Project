import pandas as pd

def merge_data(df1, df2, df3, df4, df5):
    merged_data = pd.merge(df1, df2, how='inner', on="zipcode")
    merged_data = pd.merge(merged_data, df3, how='inner', on="zipcode")

    return merged_data


