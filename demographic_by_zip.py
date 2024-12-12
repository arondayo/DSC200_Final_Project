import pandas as pd

# Function to handle Excel file processing
def process_excel():
    # Specify the Excel file path
    file_path = 'data/income_by_zip.xlsx'

    # Load the Excel file with the first row as the header
    df = pd.read_excel(file_path)

    # Drop rows two and three (index 1 and 2)
    df = df.drop([1, 2, 4])

    # List of zip codes and corresponding median incomes.
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

    # Create the dictionary mapping zip codes to median incomes
    zip_to_income = dict(zip(zip_codes, median_incomes))

    # Define the condition for columns to keep:
    condition = ~df.columns.str.startswith('Unnamed')
    condition = condition | (df.columns == df.columns[0])

    # Apply the condition to select columns
    df = df.loc[:, condition]

    df = df.drop([0])
    df = df.drop(df.index[10:])

    # Convert the dictionary to a DataFrame and ensure it matches the column structure
    income_df = pd.DataFrame([zip_to_income])

    # Add the new row to the original dataframe
    df = pd.concat([df, income_df], ignore_index=True)

    # Transpose the DataFrame so that zip codes are in the leftmost column
    df_transposed = df.transpose()

    # Set the first row (which contains the zip codes) as the new header
    df_transposed.columns = df_transposed.iloc[0]

    # Drop the first row, which is now the header row
    df_transposed = df_transposed.drop(df_transposed.index[0])

    # Reset the index to make it a regular column
    df_transposed = df_transposed.reset_index()

    # Rename other columns (update with your desired names)
    new_column_names = {
        'index': 'Zip Code',
        'White': 'White Households',
        'Black or African American': 'Black or African American Households',
        'American Indian and Alaska Native': 'American Indian and Alaska Native Households',
        'Asian': 'Asian Households',
        'Native Hawaiian and Other Pacific Islander': 'Pacific Islander Households',
        'Some other race': 'Other Race Households',
        'Two or more races': 'Mixed Race Households',
        'Hispanic or Latino origin (of any race)': 'Hispanic or Latino origin Households',
        'Median Income': 'Median Household income'
    }
    df_transposed = df_transposed.rename(columns=new_column_names)
    df_transposed.drop(["White alone, not Hispanic or Latino", "Households"], inplace=True, axis=1)

    # Remove the first 6 characters from every value in the "Zip Code" column
    df_transposed['Zip Code'] = df_transposed['Zip Code'].str[6:]

    # Export the transposed DataFrame to a new Excel file
    df_transposed.to_csv('data/cleaned_file.csv', index=True)

    print("The transposed file has been saved as 'cleaned_file.csv'")

# Function to handle CSV file processing
def process_csv():
    # Specify the CSV file path
    file_path_csv = "data/demographics_by_zip.csv"
    df2 = pd.read_csv(file_path_csv)

    # Filter the columns to keep only "Label (Grouping)" and those ending with "!!Total!!Estimate"
    columns_keep = ['Label (Grouping)'] + [col for col in df2.columns if col.endswith('!!Total!!Estimate')]

    # Select only the desired columns
    df2 = df2[columns_keep]
    df2 = df2.drop(df2.index[20:])
    df2 = df2.drop([1])
    df2.loc[1:, 'Label (Grouping)'] = df2.loc[1:, 'Label (Grouping)'].str[8:]

    df2.columns = df2.columns.str.slice(start=6, stop=11)

    # Rename the column that was the "Label (Grouping)" to "Zip Code"
    df2 = df2.rename(columns={'(Grou': 'Zip Code'})

    # Reset the index to ensure the headers are properly shifted to the first column when transposed
    df2_reset = df2.reset_index()

    # Transpose the DataFrame
    df2_transposed = df2_reset.transpose()

    # Set the first row as the header (it was originally the column names)
    df2_transposed.columns = df2_transposed.iloc[1]

    # Drop the first row as it's now redundant
    df2_transposed = df2_transposed.drop(df2_transposed.index[0])
    df2_transposed = df2_transposed.drop(df2_transposed.index[0])

    df2_transposed = df2_transposed.reset_index()

    # Create a dictionary to rename the age group columns to indicate they are population counts
    age_group_rename = {
        'index': 'Zip Code',
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

    # Now, use this dictionary to rename the columns in your DataFrame
    df2_transposed = df2_transposed.rename(columns=age_group_rename)

    # Specify the output CSV file path
    output_csv_path = "data/filtered_demographics_by_zip.csv"

    # Write the filtered DataFrame to a new CSV file
    df2_transposed.to_csv(output_csv_path, index=True)

    print(f"Filtered data has been saved to {output_csv_path}")
