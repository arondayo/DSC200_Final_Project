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

from merge_data import merge_data


def main():

    print("Data processing has begun...\n")

    #Process all 5 types of data
    df1 = process_excel()
    df2 = process_csv()
    df3 = process_api()

    #Mege Data in single CSV
    merged_data = merge_data(df1, df2, df3, df1, df1)

    #Output final CSV
    final_csv_path = "data/final_csv.csv"
    merged_data.to_csv(final_csv_path, index=False)

    #Process Pdf
    final_pdf_path = "data/final_pdf.csv"
    df_pdf = pdf_processor()
    df_pdf.to_csv(final_pdf_path, index=False)

    #Output Final PDF

    print("\nData processing complete. Output Files Final_CSV.csv and Final_PDF.csv have been created!")
    print("Have a great day!")


if __name__ == "__main__":
    main()