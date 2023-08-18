import openpyxl as xl

path = 'school list.xlsx'

wb = xl.load_workbook(path)
worksheet = wb["Sheet1"]
print(worksheet)
excel_data = list()
# iterating over the rows and
# getting value from each cell in row
for row in worksheet.iter_rows():
    row_data = list()
    for cell in row:
        row_data.append(str(cell.value))
    excel_data.append(row_data)


with open('list.txt','w') as f:
    for data in excel_data:
        f.write(f"{data[2]}\n")