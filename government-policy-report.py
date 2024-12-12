import slate3k as sl
import csv

pdfFilename = "data/housing-policy-info.pdf"
output_File = "data/chicago-housing-policy-report.csv"


with open(pdfFilename, "rb") as pdfFileObject:
    # Getting raw data
    doc = sl.PDF(pdfFileObject)

    #table we want is on page 14 (index 13)
    table_page = doc[13]

    page_lines = table_page.split("\n")

    start_index = page_lines.index('2000')  # Find the index of the starting string
    end_index = page_lines.index('Housing Market Trends')
    filtered_data = page_lines[start_index:end_index]

    for item in filtered_data:
        if item == '':
            filtered_data.remove(item)


    filtered_data[3] = "Percent Change from 2000 to 2010"
    filtered_data[4] = "Percent Change from 2010 to Current"
    headers = filtered_data[:5]
    headers.insert(0, "Measurement")

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

    print(rows)

    with open (output_File, "w", newline="") as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)
        csvFile.close()
        print("Data outputted successfully!")





