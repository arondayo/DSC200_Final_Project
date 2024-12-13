#Import slate and pandas for pdf data access and data cleaning
import slate3k as sl
import pandas as pd

"""
This function accesses a pdf file and pulls data off a chart that it contains. The chosen pdf file is a report from the US department of 
Housing and Urban Development. It is a comprehensive housing market analysis and we were able to find a chart that deals with many
housing market statistics over the past 30 years in downtown chicago. We are keeping this PDF csv seperate from the merged data csv 
because we were unable to find a pdf with the needed level of granularity. We use slate3k to access and extract the data from the PDF. 
Then we used pandas to convert it to a dataframe and clean the data before returning it back to main. 
"""

def pdf_processor():

    #Create variable for the pdf data file
    pdfFilename = "data/housing-policy-info.pdf"

    #Open the file with binary read access
    with open(pdfFilename, "rb") as pdfFileObject:
        #Save raw data
        doc = sl.PDF(pdfFileObject)

        #The table we want is on page 14 (index 13)
        table_page = doc[13]

        page_lines = table_page.split("\n")

        #Find the index of the starting string and ending string we need
        start_index = page_lines.index('2000')
        end_index = page_lines.index('Housing Market Trends')
        filtered_data = page_lines[start_index:end_index]

        #Remove extra spaces
        for item in filtered_data:
            if item == '':
                filtered_data.remove(item)

        #Rename and clean column headings for extra clarity
        filtered_data[3] = "Percent Change from 2000 to 2010"
        filtered_data[4] = "Percent Change from 2010 to Current"
        headers = filtered_data[:5]
        headers.insert(0, "Year")

        #Nested for loop to organize the data
        rows = []
        row = []
        for item in filtered_data[5:]:
            if item[0].isalpha():
                if row:
                    rows.append(row)
                row = [item]
            else:
                row.append(item)

        if row:
            rows.append(row)

        #Transpose the data to ensure data consistency
        transposed_data = list(zip(*([headers] + rows)))

        #Create a dataframe for the data and return it back to main for output
        transposed_data = pd.DataFrame(data=transposed_data[1:], columns=transposed_data[0])
        return transposed_data




