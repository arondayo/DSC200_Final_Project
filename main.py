"""
Group 1 Final Project: Steven Weil, Aaron Anderson
Chicago, Illinois
12/12/2024
DSC 200
"""
#Import all the necessary libraries

from api_housing_trends import process_api
from demographic_by_zip import process_excel, process_csv
from government_policy_report import pdf_processor
import pandas as pd
from merge_data import merge_data
from scrape_cleaning import scrape_clean


"""
We are the doing out project on the area Chicago, Illinois. We have chosen to filter all of the data based on the zipcodes in Chicago and 
have found many different data sources with relevant information. This program consists of 8 python files all of which have header comments to
explain their individual function. 

This is the main function for the program. It allows the user to track some of the steps that are being completed through messages 
printed to the screen. It also collects all of the dataframes and calls of the methods to process and merge the data. Finally, 
It outputs the data to two csv files. 
"""
def main():

    print("Data processing has begun...\n")

    #Process all the types of data
    df1 = process_excel()
    print("Excel Processing Complete!")
    df2 = process_csv()
    print("CSV Processing Complete!")
    df3 = process_api()
    print("API Processing Complete!")
    df4 = scrape_clean()[['zipcode','owned_property_avg_price','rental_property_avg_price']]

    #Merge Data in single CSV
    merged_data = merge_data(df1, df2, df3, df4)
    print("Data Merge Complete!")

    #The calculated fields (owned_property_avg_price and rental_property_avg_price) did not have data for some specific zip codes
    #so, rather than throwing out all of the data from that row, we replaced the null value with a zero to keep the data type in
    #the columns consistent
    merged_data.fillna(0, inplace=True)


    #Output final CSV
    final_csv_path = "data/final_csv.csv"
    merged_data.to_csv(final_csv_path, index=False)


    #Process Pdf
    final_pdf_path = "data/final_pdf_data.csv"
    df_pdf = pdf_processor()
    print("PDF Processing Complete!")

    #Output Final PDF
    df_pdf.to_csv(final_pdf_path, index=False)

    #Print out successful output message
    print("\nAll Data processing complete. Output Files final_csv.csv and final_pdf_data.csv have been created!")
    print("Have a great day!")


if __name__ == "__main__":
    main()