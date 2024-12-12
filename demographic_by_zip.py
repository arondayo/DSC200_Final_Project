import openpyxl
import csv
import pandas as pd

# Specify the Excel file path
file_path = 'data/income_by_zip.xlsx'

# Load the Excel file with the first row as the header
df = pd.read_excel(file_path)

# Drop rows two and three (index 1 and 2)
df = df.drop([1, 2, 4])

# List of zip codes
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

# List of median incomes corresponding to the zip codes
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
# 1. Keep columns where the header does not start with 'Unnamed'
condition = ~df.columns.str.startswith('Unnamed')
# Ensure the first column is always kept
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

# Rename the column to give it a proper header
df_transposed = df_transposed.rename(columns={'index': 'Zip Codes'})


# Export the transposed DataFrame to a new Excel file
df_transposed.to_excel('data/cleaned_file.xlsx', index=True)

print("The transposed file has been saved as 'cleaned_file.xlsx'")
