import openpyxl as xl
from master.models import Application,FinancialYear

def file_handler(file_name):
    workbook = xl.load_workbook(file_name)
    worksheet = workbook.active
    for i in range(2,worksheet.max_column+1):
        name = worksheet.cell(row=i,column=2).value
        admission_number = worksheet.cell(row=i,column=3).value
        ward = worksheet.cell(row=i,column=4).value
        gender = worksheet.cell(row=i,column=5).value
        disability_status = worksheet.cell(row=i,column=6).value
        family_status = worksheet.cell(row=i,column=7).value
        institution = worksheet.cell(row=i,column=8).value
        school_type = worksheet.cell(row=i,column=9).value
        bank = worksheet.cell(row=i,column=10).value
        account = worksheet.cell(row=i,column=11).value
        branch = worksheet.cell(row=i,column=12).value
        amount = worksheet.cell(row=i,column=13).value
        if (name and admission_number and ward and gender and disability_status and family_status and institution and school_type and bank and account and branch and amount):
            financial_year = FinancialYear.objects.filter(is_active=True)
            application = Application.objects.create(
                full_name = name,
                birth_cert_no = 000000000,
                admission = admission_number,
                ward = ward,
                gender = gender,
                disability_status = disability_status,
                family_status = family_status,
                institution = institution,
                bank = bank,
                account = account,
                branch = branch,
                amount = amount,
                financial_year = financial_year 
            )
            application.save()
        else:
            return False,"There are some data missing! Data not saved"
    return True, "Data successfully saved!"

def file_creator(applications):
    wb = xl.Workbook()
    ws = wb.active
    c1 = ws.cell(row=1,column=1)
    c1.value = 'Full Name'
    c2 = ws.cell(row=1,column=2)
    c2.value = 'Admission/Registration Number'
    c3 = ws.cell(row=1,column=3)
    c3.value = 'Gender'
    c4 = ws.cell(row=1,column=4)
    c4.value = 'Amount'

    i = 2
    for data in applications:
        c1 = ws.cell(row=i,column=1)
        c1.value = data.full_name
        c2 = ws.cell(row=i,column=2)
        c2.value = data.admission_no
        c3 = ws.cell(row=i,column=3)
        c3.value = data.get_gender_display()
        c4 = ws.cell(row=i,column=4)
        c4.value = data.amount
        i += 1
    
    wb.save('Students List.xlsx')