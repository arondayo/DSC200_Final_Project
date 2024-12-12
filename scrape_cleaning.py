import numpy as np

from apartments_dot_com_scrape import  apartments_scrape
from bestchicagoproperties_dot_com_scrape import chicago_properties_scrape

import pandas as pd

def scrape_clean() -> pd.DataFrame:
    # checking to see scrape output csv files exist to save the time instead of scraping every time if they already exist
    try: # access / create apartments.com scrape csv
        print("Existing Apartments.com scrape file found...")
        apartments_df = pd.read_csv('data/apartments.com_chicago-il_scrape.csv')
    except FileNotFoundError:
        print("No existing scrape file found... Starting scrape of <https://www.apartments.com/chicago-il/>")
        apartments_df = apartments_scrape('https://www.apartments.com/chicago-il/')

    try: # access / create bestchicagoproperties.com scrape
        print("Existing bestchicagoproperties.com scrape file found...")
        properties_df = pd.read_csv('data/bestchicagoproperties.com_scrape.csv')
    except FileNotFoundError:
        print("No existing scrape file found... Starting scrape of <bestchicagoproperties.com>")
        properties_df = chicago_properties_scrape()


    # clean out non-currency entries for price from the dfs
    apartments_df = apartments_df[~apartments_df['price_low'].str.contains('[^$0-9, ]')]
    properties_df = properties_df[~properties_df['price'].str.contains('[^$0-9, ]')]

    # convert the price cols to actual numbers
    apartments_df['price_low'] = (apartments_df['price_low']
                                      .str.replace(r'[\$]', '', regex=True)
                                      .str.replace(r'[\,]', '', regex=True)
                                      .str.replace(r'[ ]', '', regex=True)
                                      ).astype(int)
    apartments_df['price_high'] = (apartments_df['price_high']
                                      .str.replace(r'[\$]', '', regex=True)
                                      .str.replace(r'[\,]', '', regex=True)
                                      .str.replace(r'[ ]', '', regex=True)
                                      ).astype(int)
    properties_df['price'] = (properties_df['price']
                                      .str.replace(r'[\$]', '', regex=True)
                                      .str.replace(r'[\,]', '', regex=True)
                                      .str.replace(r'[ ]', '', regex=True)
                                      ).astype(int)

    # computing average price for the price ranges given from apartments.com
    apartments_df['price_avg'] = apartments_df[['price_low', 'price_high']].mean(axis=1)


    # generating pivot table for both df to get the average price of rental and owned properties per zipcode
    apartments_pt = pd.pivot_table(apartments_df, index=['zipcode'], values=['price_avg'], aggfunc='mean')
    apartments_avg_df = apartments_pt.reset_index().rename(columns={'price_avg': 'rental_property_avg_price'})

    properties_pt = pd.pivot_table(properties_df, index=['zipcode'], values=['price'], aggfunc='mean')
    properties_avg_df = properties_pt.reset_index().rename(columns={'price': 'owned_property_avg_price'})


    # creating output df
    output_df = pd.merge(apartments_avg_df, properties_avg_df, on='zipcode', how='outer').sort_values(by='zipcode')

    # formatting output df data
    # (pulled from stackexchange) formats the final number to have at most 2 decimal places
    output_df['owned_property_avg_price'] = output_df['owned_property_avg_price'].apply(lambda x: float("{:.2f}".format(x)))
    output_df['rental_property_avg_price'] = output_df['rental_property_avg_price'].apply(lambda x: float("{:.2f}".format(x)))
    return output_df

if __name__ == '__main__':
    df = scrape_clean()
    # df.to_csv('data/clean_scrape_data.csv', index=False)