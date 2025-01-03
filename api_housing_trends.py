#Import libraries to access, extract, organize, and clean data
import requests
import pandas as pd

"""
This function accesses the census.gov API in order to retrieve information about housing market trends by zip code in Chicago. \
It provides information about the amount of housing units available in the zip code and what percent of rental and owned properties 
are vacant. We use requests and dictionary of the zip codes to pull in the data from all the pages. Then we clean and organize the data 
before sending it back to main for merging. 
"""

def process_api():
    #Create dictionary for zipcodes we will need to page through using the api and requests
    zip_codes = [
        60601, 60602, 60603, 60604, 60605, 60606, 60607, 60608, 60609, 60610, 60611, 60612,
        60613, 60614, 60615, 60616, 60617, 60618, 60619, 60620, 60621, 60622, 60623, 60624,
        60625, 60626, 60628, 60629, 60630, 60631, 60632, 60633, 60634, 60636, 60637, 60638,
        60639, 60640, 60641, 60642, 60643, 60644, 60645, 60646, 60647, 60649, 60651, 60652,
        60653, 60654, 60655, 60656, 60657, 60659, 60660, 60661
    ]
    #Send GET request to the API and protect against unsuccessful connections
    try:
        table_data = []
        headers = None
        #Loop through each zip code and get the data for each one
        for zip_code in zip_codes:
            base_url = 'https://api.census.gov/data/2022/acs/acs5/profile?get=NAME,DP04_0001E,DP04_0003E,DP04_0004E,DP04_0005E&for=zip%20code%20tabulation%20area:{0}&key=ec274c4d126c681dd7359bde3ee46e4e5a684c02'.format(zip_code)
            response = requests.get(base_url)
            data = response.json()

            #Check if the data is not empty or if it has the correct format
            if data:
                if headers is None:
                    #Set the headers from the first response
                    headers = data[0]
                #Append the data
                table_data.append(data[1])

        #Reorganize Column Names to be more clear and consistent
        headers[0] = "Census Zip Code Tag"
        headers[1] = "Total Housing Units"
        headers[2] = "Vacant Housing Units"
        headers[3] = "Homeowner Vacancy Rate"
        headers[4] = "Rental Vacancy Rate"
        headers[5] = "zipcode"

        #Save the data as a dataframe and change the zip code values to ints for later merging
        df = pd.DataFrame(data=table_data, columns=headers)
        df['zipcode'] = df['zipcode'].astype(int)
        #Drop unnecessary column
        df = df.drop(columns='Census Zip Code Tag')

        #Retun dataframe for merging
        return df
    #Print out error message if connection is unsuccessful
    except requests.exceptions.RequestException as e:
        print('An error occurred:', e)


