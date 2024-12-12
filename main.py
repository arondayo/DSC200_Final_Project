"""
Group 1 Final Project: Steven Weil, Aaron Anderson
Chicago, Illinois
12/12/2024
DSC 200


"""


from api_housing_trends import process_api
from demographic_by_zip import process_excel, process_csv
from government_policy_report import pdf_processor
import pandas as pd


def main():

    print("Data processing has begun...\n")

    #Process all 5 types of data
    process_excel()
    process_csv()
    process_api()

    #Mege Data in single CSV

    #Output final CSV


    #Process Pdf
    pdf_processor()

    #Output Final PDF

    print("\nData processing complete. Output Files Final_CSV.csv and Final_PDF.csv have been created!")
    print("Have a great day!")


if __name__ == "__main__":
    main()