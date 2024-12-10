import time, re
from bs4 import BeautifulSoup as bSoup
from selenium import webdriver
import pandas as pd

def apartments_scrape(url: str, pages: int = None) -> pd.DataFrame:
    # receives url and number of pages as arguments (if left empty will scrape all available pages)
    #   url examples
    #       https://www.apartments.com/new-york-ny/
    #       https://www.apartments.com/chicago-il/

    if pages is None: # determining number of pages
        driver = webdriver.Chrome()
        driver.get(url)
        pages = int(bSoup(driver.page_source, 'html.parser').find('span', class_='pageRange').text.split(' ')[-1])
        print(f'{pages} pages found for {url.split('/')[3]}')


    headers = ['name', 'address', 'zipcode', 'price_low', 'price_high', 'layout', 'amenities', 'link', 'phone_number']
    rows = []

    for page_number in range(1, pages + 1):
        url_ = f'{url}{page_number}/'
        driver = webdriver.Chrome()
        driver.get(url_)
        time.sleep(1)
        print(f'Extracting Apartments.com listings for {url.split('/')[3]} page {page_number}')

        soup = bSoup(driver.page_source, 'html.parser')
        driver.close()

        listings_ul = soup.find('div', class_='placardContainer').find_all('li', class_="mortar-wrapper")
        for li in listings_ul:
            # Name
            name = li.find('span', class_='js-placardTitle title').text

            # address + zipcode
            address_raw = li.find('div', class_='property-address js-url') # normal address locating
            if not address_raw:
                address_raw = li.find('p', class_='property-address js-url') # alt address locating
                if not address_raw:
                    if re.match(r'([0-9 .\-\'A-z]+, [A-z \-\']+, [A-Z]{2} [0-9]{5})', name): # attempts to parse address out of title if other methods fail
                        address_raw_text = re.sub(r'\n', '', name).strip()
                        address = address_raw_text[:-6]
                        zipcode = address_raw_text[-5:]
                    else:
                        address = None
                        zipcode = None
                else:
                    address_raw_text = re.sub(r'\n','', address_raw.text).strip()
                    address = address_raw_text[:-6]
                    zipcode = address_raw_text[-5:]
            else:
                address_raw_text = re.sub(r'\n', '', address_raw.text).strip()
                address = address_raw_text[:-6]
                zipcode = address_raw_text[-5:]


            # prices (low + high)
            prices_raw = li.find('p', class_='property-pricing')
            if not prices_raw:
                prices_raw = li.find('p', class_='property-rents')
                if not prices_raw:
                    prices_raw = li.find('div', class_='price-range')
                    if not prices_raw:
                        price_low = None
                        price_high = None
                    else:
                        prices = prices_raw.text.split(' - ')
                        if len(prices) == 2:
                            price_low = prices[0]
                            price_high = prices[1]
                        else:
                            price_low = prices[0]
                            price_high = prices[0]
                else:
                    prices = prices_raw.text.split(' - ')
                    if len(prices) == 2:
                        price_low = prices[0]
                        price_high = prices[1]
                    else:
                        price_low = prices[0]
                        price_high = prices[0]
            else:
                prices = prices_raw.text.split(' - ')
                if len(prices) == 2:
                    price_low = prices[0]
                    price_high = prices[1]
                else:
                    price_low = prices[0]
                    price_high = prices[0]


            # layout
            layout_raw = li.find('p', class_='property-beds')
            if not layout_raw:
                layout_raw = li.find('div', class_='bed-range')
                if not layout_raw:
                    layout = None
                else:
                    layout = layout_raw.text.strip()
            else:
                layout = layout_raw.text.strip()

            # amenities
            amenities_raw = li.find('p', class_='property-amenities')
            if not amenities_raw:
                amenities = None
            else:
                # amenities had items split into individual <spans>, that get interpreted as an \n, this cleans those out and formats
                amenities = re.sub(r'\n', ', ', # second replacement
                                   re.sub(r'^\n|\n$', '', # first replacement
                                          amenities_raw.text))

            # link
            link = li.find('a', class_='property-link').get('href')

            # phone number
            property_actions = li.find('div', class_='property-actions')
            if not property_actions:
                phone_number = None
            else:
                phone_number_raw = property_actions.find('a')
                phone_number = None if not phone_number_raw else re.sub(r'\n', '', phone_number_raw.text)


            row = [name, address, zipcode, price_low, price_high, layout, amenities, link, phone_number]
            rows.append(row)
            # print(row)

    df = pd.DataFrame(rows, columns=headers)
    print(f'results saved to: data/apartments.com_{url.split('/')[3]}_scrape.csv')
    df.to_csv(f'data/apartments.com_{url.split('/')[3]}_scrape.csv', index=False)
    return df

if __name__ == '__main__':
    apartments_scrape('https://www.apartments.com/chicago-il/')