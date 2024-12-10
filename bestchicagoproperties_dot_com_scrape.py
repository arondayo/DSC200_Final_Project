import time, re
from http.client import responses

from bs4 import BeautifulSoup as bSoup
import requests as rq
# from selenium import webdriver
import pandas as pd

def chicago_properties_scrape() -> pd.DataFrame:
    chicago_zip_codes = [
        60290, 60601, 60602, 60603, 60604, 60605, 60606, 60607, 60608, 60610, 60611, 60614, 60615, 60618, 60619,
        60622, 60623, 60624, 60628, 60609, 60612, 60613, 60616, 60617, 60620, 60621, 60625, 60626, 60629, 60630,
        60632, 60636, 60637, 60631, 60633, 60634, 60638, 60641, 60642, 60643, 60646, 60647, 60652, 60653, 60656,
        60660, 60661, 60664, 60639, 60640, 60644, 60645, 60649, 60651, 60654, 60655, 60657, 60659, 60666, 60668,
        60673, 60677, 60669, 60670, 60674, 60675, 60678, 60680, 60681, 60682, 60686, 60687, 60688, 60689, 60694,
        60695, 60697, 60699, 60684, 60685, 60690, 60691, 60693, 60696, 60701
    ]

    headers = ['address', 'zipcode', 'price', 'housing_type', 'status', 'layout', 'link']
    rows = []

    print('Scraping data from bestchicagoproperties.com')
    print(f'Scanning through {len(chicago_zip_codes)} zipcodes...\n')
    print('Zip code\tListings')
    for zip_code in chicago_zip_codes:
        time.sleep(1)
        url = f'https://bestchicagoproperties.com/property-search/chicago-real-estate-for-sale-by-zip-code/{zip_code}-chicago-homes-for-sale/'
        response = rq.get(url)
        soup = bSoup(response.text, 'html.parser')

        listings = soup.find_all('div', class_='sidx-require-auth')
        print(f'{zip_code}\t\t{len(listings)}')

        for listing in listings:
            # address
            raw_address = listing.find('div', class_='sidx-listing-heading').text
            address = re.sub(r'Chicago', r', Chicago',
                re.sub(rf'({str(zip_code)})', rf'{zip_code} ', raw_address)).strip()

            # zip, price, housing_type, status
            zipcode = zip_code
            price = listing.find('div', class_='sidx-price').text
            housing_type = re.sub(r' For Sale','', listing.find('div', class_='sidx-sale-type sidx-for-sale').text)
            status = listing.find('div', class_='sidx-mls-info').text

            # layout
            raw_layout = listing.find_all('div', class_='sidx-info-block')
            layout = []
            for entry in raw_layout:
                layout.append(entry.text)

            # link
            link = f'https://bestchicagoproperties.com{listing.find('a').get('href')}'

            row = [address, zipcode, price, housing_type, status, layout, link]
            rows.append(row)


    df = pd.DataFrame(rows, columns=headers)
    print(f'results saved to: data/bestchicagoproperties.com_scrape.csv')
    df.to_csv(f'data/bestchicagoproperties.com_scrape.csv', index=False)
    return df

if __name__ == '__main__':
    chicago_properties_scrape()
