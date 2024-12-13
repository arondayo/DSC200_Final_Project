# Project requirements

Students will work in pairs to acquire, clean, and integrate datasets related to housing trends in a U.S. region or state of their choice. The focus will be on building a unified, clean, and ready-to-analyze dataset, demonstrating mastery of data wrangling techniques.

- **Excel Files:** 
	- Import neighborhood demographic data specific to your chosen region.
		- Download Demographics Data (Excel): https://www.census.gov/data.html
- **CSV Files:** 
	- Import median housing prices and rental costs for your chosen region.
		- Download Housing Prices Data (CSV): https://www.zillow.com/research/data/
		- Download Rental Costs Data (CSV): https://www.kaggle.com/datasets
- **Web Scraping:** 
	- Extract rental listings and descriptions from a real estate website such as Craigslist or Apartments.com for your selected area.
- **API Access:** 
	- Retrieve recent housing market trends specific to your region using Zillow or a similar platform API.
		- Zillow API Documentation: https://www.zillow.com/howto/api/APIOverview.htm
- **PDF Files:** 
	- Extract relevant data from government housing policy reports specific to your chosen area. 
		- Download Housing Policy Report Example (PDF): https://www.huduser.gov/portal/home.html

---

# Zip Codes of Chicago

`[60290, 60601, 60602, 60603, 60604, 60605, 60606, 60607, 60608, 60610, 60611, 60614, 60615, 60618, 60619, 60622, 60623, 60624, 60628, 60609, 60612, 60613, 60616, 60617, 60620, 60621, 60625, 60626, 60629, 60630, 60632, 60636, 60637, 60631, 60633, 60634, 60638, 60641, 60642, 60643, 60646, 60647, 60652, 60653, 60656, 60660, 60661, 60664, 60639, 60640, 60644, 60645, 60649, 60651, 60654, 60655, 60657, 60659, 60666, 60668, 60673, 60677, 60669, 60670, 60674, 60675, 60678, 60680, 60681, 60682, 60686, 60687, 60688, 60689, 60694, 60695, 60697, 60699, 60684, 60685, 60690, 60691, 60693, 60696, 60701]`

# Web Scraping

end goal: aggregate average prices (rental apartments, purchasing home) per zip code for merging
	`(zipcode, rental_property_avg_price, owned_property_avg_price)`

## apartments.com

Pages (1-18) (I've implemented a way to find the # of pages automatically)
Pull:
	
 `[name, address, zipcode, price_low, price_high, layout, amenities, link, phone_number]`

https://www.apartments.com/chicago-il/{page_number}/


## bestchicagoproperties.com

Pull all the available data from the first page from each of the zip codes above (an account is required to see more than the first page) 

Pull:

 `['address', 'zipcode', 'price', 'housing_type', 'status', 'layout', 'link']`

 https://bestchicagoproperties.com/property-search/chicago-real-estate-for-sale-by-zip-code/{zip_code}-chicago-homes-for-sale/
