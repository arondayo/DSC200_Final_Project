import numpy as np

from apartments_dot_com_scrape import  apartments_scrape
from bestchicagoproperties_dot_com_scrape import chicago_properties_scrape

import pandas as pd

def scrape_clean() -> pd.DataFrame:
    try: # access / create apartments.com scrape csv
        apartments_df = pd.read_csv('data/apartments.com_chicago-il_scrape.csv')
    except FileNotFoundError:
        print("File not found... Starting scrape of <https://www.apartments.com/chicago-il/>")
        apartments_df = apartments_scrape('https://www.apartments.com/chicago-il/')

    try: # access / create bestchicagoproperties.com scrape
        properties_df = pd.read_csv('data/bestchicagoproperties.com_scrape.csv')
    except FileNotFoundError:
        print("File not found... Starting scrape of <bestchicagoproperties.com>")
        properties_df = chicago_properties_scrape()

    # print('\n================================')
    # print('apartments data:')
    # print(apartments_df.info())
    # print('\nproperties data:')
    # print(properties_df.info())

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

    # print('\napartments_df')
    # print(apartments_df.loc[:, ['zipcode', 'price_low', 'price_high']])
    # print('\nproperties_df')
    # print(properties_df.loc[:, ['zipcode', 'price']])

    properties_pt = pd.pivot_table(properties_df, index=['zipcode'], values=['price'], aggfunc='mean')
    print(properties_pt.reset_index().rename(columns={'price': 'owned_avg'}))

    # todo average price_low & price_high for apartments_df or not?

    # todo final output: average pricing per zipcode, both rental and owned property
    #  ['zipcode', 'rental_avg', '?rental_std_dev?', 'owned_avg', '?owned_std_dev?']

    print('\n================================')
    print('apartments data after:')
    print(apartments_df.info())
    print('\nproperties data after:')
    print(properties_df.info())

    return 0

if __name__ == '__main__':
    scrape_clean()