import requests
import csv

zip_codes = [
    60601, 60602, 60603, 60604, 60605, 60606, 60607, 60608, 60609, 60610, 60611, 60612,
    60613, 60614, 60615, 60616, 60617, 60618, 60619, 60620, 60621, 60622, 60623, 60624,
    60625, 60626, 60628, 60629, 60630, 60631, 60632, 60633, 60634, 60636, 60637, 60638,
    60639, 60640, 60641, 60642, 60643, 60644, 60645, 60646, 60647, 60649, 60651, 60652,
    60653, 60654, 60655, 60656, 60657, 60659, 60660, 60661
]

try:
    table_data = []
    headers = None  # We'll set the headers once we get the first response

    for zip_code in zip_codes:
        base_url = 'https://api.census.gov/data/2022/acs/acs5/profile?get=NAME,DP04_0001E,DP04_0003E,DP04_0004E,DP04_0005E&for=zip%20code%20tabulation%20area:{0}&key=ec274c4d126c681dd7359bde3ee46e4e5a684c02'.format(
            zip_code)
        response = requests.get(base_url)
        data = response.json()

        # Check if the data is not empty or if it has the correct format
        if data:
            if headers is None:
                # Set the headers from the first response
                headers = data[0]
            # Append the data (excluding the header row)
            table_data.append(data[1])

    # Write the data to a CSV file
    with open("data/housing-trends.csv", "w", newline="", encoding="utf-8") as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(headers)  # Write the headers first
        csvWriter.writerows(table_data)  # Write the data rows
        print("Data saved to data/housing-trends.csv successfully!")

except requests.exceptions.RequestException as e:
    print('An error occurred:', e)
