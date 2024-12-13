#Import pandas to clean and organize the data
import pandas as pd


"""
This function handles the excel file processing. The chosen file provides demographic information about the Zip codes of Chicago.
It creates a dataframe for the excel file data and cleans it for later merging.  
The excel file was pulled from the census.gov database and provides information about Chicago Households. 
We have chosen to focus on the median income per household and data about the ethnicity of households. We used pandas
to read in the excel file. The format of the file was a bit strange and we needed to do alot of dropping, transposing, and
other data manipulation to get the end product. Specifically, for the Median income we manually created a dictionary and mapped it to its corresponding
zip code. The reasoning behind this was the way the original file was formatted, it was almost impossible to get the data to line up 
correctly otherwise. Once, that was in place, Median income and all the other columns were cleaned with pandas normally. 

"""

#Function to handle the Excel File Processing
def process_excel():
    #Create the file path variable
    file_path = 'data/income_by_zip.xlsx'

    #Load the excel file into a dataframe
    df = pd.read_excel(file_path)

    #Drop rows at index, 1, 2, 4 => these were formatting rows that contained no info
    df = df.drop([1, 2, 4])

    #List of zip codes and corresponding median incomes.
    zip_codes = [
        "Unnamed: 0", "ZCTA5 60601", "ZCTA5 60602", "ZCTA5 60603", "ZCTA5 60604", "ZCTA5 60605", "ZCTA5 60606",
        "ZCTA5 60607", "ZCTA5 60608", "ZCTA5 60609", "ZCTA5 60610", "ZCTA5 60611", "ZCTA5 60612",
        "ZCTA5 60613", "ZCTA5 60614", "ZCTA5 60615", "ZCTA5 60616", "ZCTA5 60617", "ZCTA5 60618",
        "ZCTA5 60619", "ZCTA5 60620", "ZCTA5 60621", "ZCTA5 60622", "ZCTA5 60623", "ZCTA5 60624",
        "ZCTA5 60625", "ZCTA5 60626", "ZCTA5 60628", "ZCTA5 60629", "ZCTA5 60630", "ZCTA5 60631",
        "ZCTA5 60632", "ZCTA5 60633", "ZCTA5 60634", "ZCTA5 60636", "ZCTA5 60637", "ZCTA5 60638",
        "ZCTA5 60639", "ZCTA5 60640", "ZCTA5 60641", "ZCTA5 60642", "ZCTA5 60643", "ZCTA5 60644",
        "ZCTA5 60645", "ZCTA5 60646", "ZCTA5 60647", "ZCTA5 60649", "ZCTA5 60651", "ZCTA5 60652",
        "ZCTA5 60653", "ZCTA5 60654", "ZCTA5 60655", "ZCTA5 60656", "ZCTA5 60657", "ZCTA5 60659",
        "ZCTA5 60660", "ZCTA5 60661"
    ]
    median_incomes = [
        "Median Income", "121,294", "167,617", "124,888", "76,667", "116,462", "133,333", "119,500", "66,821", "47,209", "106,277",
        "126,812", "58,858", "92,238", "135,364", "56,518", "72,326", "51,203", "100,976", "42,802", "46,472",
        "30,163", "119,134", "37,814", "31,768", "83,527", "56,145", "48,601", "53,318", "91,135", "112,974",
        "53,966", "54,956", "82,771", "30,451", "37,247", "85,374", "54,969", "69,397", "79,884", "137,853",
        "80,461", "34,177", "73,726", "112,283", "97,550", "39,862", "48,532", "76,300", "35,136", "138,279",
        "115,324", "82,992", "105,428", "64,202", "63,596", "139,748"
    ]

    #Create the dictionary mapping zip codes to median incomes
    zip_to_income = dict(zip(zip_codes, median_incomes))

    #Define the condition to create a boolean series to help filter out columns that need to be dropped:
    condition = ~df.columns.str.startswith('Unnamed')
    condition = condition | (df.columns == df.columns[0])

    #Use the boolean series to filter out the unnecessary columns.
    df = df.loc[:, condition]

    #Drop other rows with unnecessary data.
    df = df.drop([0])
    df = df.drop(df.index[10:])

    #Convert the dictionary into a dataframe
    income_df = pd.DataFrame([zip_to_income])

    #Add the new median income column as the first column
    df = pd.concat([income_df, df], ignore_index=True)

    #Transpose the DataFrame so that each zip code is a row
    df_transposed = df.transpose()

    #Set the first row to be the new headers
    df_transposed.columns = df_transposed.iloc[0]

    #Drop the first row, which is now the header row
    df_transposed = df_transposed.drop(df_transposed.index[0])

    #Reset the index
    df_transposed = df_transposed.reset_index()

    #Rename other columns to clarify data
    new_column_names = {
        'index': 'zipcode',
        'White': 'White Households',
        'Black or African American': 'Black or African American Households',
        'American Indian and Alaska Native': 'American Indian and Alaska Native Households',
        'Asian': 'Asian Households',
        'Native Hawaiian and Other Pacific Islander': 'Pacific Islander Households',
        'Some other race': 'Other Race Households',
        'Two or more races': 'Mixed Race Households',
        'Hispanic or Latino origin (of any race)': 'Hispanic or Latino origin Households',
        'Median Income': 'Median Household income (Dollars)'
    }
    #Update the names and drop unneeded data
    df_transposed = df_transposed.rename(columns=new_column_names)
    df_transposed.drop(["White alone, not Hispanic or Latino", "Households"], inplace=True, axis=1)

    #Isolate the zip code for later merging and parse it to an int
    df_transposed['zipcode'] = df_transposed['zipcode'].str[6:].astype(int)
    df_transposed['zipcode'] = df_transposed['zipcode'].astype(int)

    #Return the dataframe for merging
    return df_transposed


"""
This function handles the CSV file processing. It takes a CSV file that also contains information about the demographic data in Chicago
by zip codes and translates it into a dataframe for later merging. The CSV was found on census.gov and the data pertains to 
population and age information about each zip code in Chicago. It gives the amount of people total and per age range in the given 
zip code. We used pandas to clean the data and return it back to main. 
"""


def process_csv():
    # Create the file path variable
    file_path_csv = "data/demographics_by_zip.csv"
    # Create dataframe with CSV data
    df2 = pd.read_csv(file_path_csv)

    # Filter the columns to keep only the needed data
    columns_to_keep = []
    for col in df2.columns:
        if col.endswith('!!Total!!Estimate'):
            columns_to_keep.append(col)

    columns_to_keep = ['Label (Grouping)'] + columns_to_keep

    # Filter data to needed columns
    df2 = df2[columns_to_keep]
    # Drop unnecessary rows
    df2 = df2.drop(df2.index[20:])
    df2 = df2.drop([1])

    # Cut extra info out of strings to prepare for later merging
    df2.loc[1:, 'Label (Grouping)'] = df2.loc[1:, 'Label (Grouping)'].str[8:]
    df2.columns = df2.columns.str.slice(start=6, stop=11)

    # Reset the index
    df2 = df2.reset_index()

    # Transpose df2
    df2_transposed = df2.transpose()

    # Set the first row as the header
    df2_transposed.columns = df2_transposed.iloc[1]

    # Drop the first row, which is now the header row
    df2_transposed = df2_transposed.drop(df2_transposed.index[0:2])
    # Reset the index
    df2_transposed = df2_transposed.reset_index()

    # Create a dictionary to rename the age group columns to better indicate they are population counts
    age_group_rename = {
        'index': 'zipcode',
        'Under 5 years': 'Population Under 5 years',
        '5 to 9 years': 'Population 5 to 9 years',
        '10 to 14 years': 'Population 10 to 14 years',
        '15 to 19 years': 'Population 15 to 19 years',
        '20 to 24 years': 'Population 20 to 24 years',
        '25 to 29 years': 'Population 25 to 29 years',
        '30 to 34 years': 'Population 30 to 34 years',
        '35 to 39 years': 'Population 35 to 39 years',
        '40 to 44 years': 'Population 40 to 44 years',
        '45 to 49 years': 'Population 45 to 49 years',
        '50 to 54 years': 'Population 50 to 54 years',
        '55 to 59 years': 'Population 55 to 59 years',
        '60 to 64 years': 'Population 60 to 64 years',
        '65 to 69 years': 'Population 65 to 69 years',
        '70 to 74 years': 'Population 70 to 74 years',
        '75 to 79 years': 'Population 75 to 79 years',
        '80 to 84 years': 'Population 80 to 84 years',
        '85 years and over': 'Population 85 years and over'
    }

    # Update the df with the new column names
    df2_transposed = df2_transposed.rename(columns=age_group_rename)
    # Parse the zip code strings to ints for later merging
    df2_transposed['zipcode'] = df2_transposed['zipcode'].astype(int)

    # Return the dataframe for merging
    return df2_transposed


