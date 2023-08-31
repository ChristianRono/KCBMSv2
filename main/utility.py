import pandas as pd
# import openpyxl as xl

from master.models import Application,FinancialYear
from collections import defaultdict
from django.apps import apps


class BulkCreateManager(object):
    """
    This helper class keeps track of ORM objects to be created for multiple
    model classes, and automatically creates those objects with `bulk_create`
    when the number of objects accumulated for a given model class exceeds
    `chunk_size`.
    Upon completion of the loop that's `add()`ing objects, the developer must
    call `done()` to ensure the final set of objects is created for all models.
    """

    def __init__(self, chunk_size=100):
        self._create_queues = defaultdict(list)
        self.chunk_size = chunk_size

    def _commit(self, model_class):
        model_key = model_class._meta.label
        model_class.objects.bulk_create(self._create_queues[model_key])
        self._create_queues[model_key] = []

    def add(self, obj):
        """
        Add an object to the queue to be created, and call bulk_create if we
        have enough objs.
        """
        model_class = type(obj)
        model_key = model_class._meta.label
        self._create_queues[model_key].append(obj)
        if len(self._create_queues[model_key]) >= self.chunk_size:
            self._commit(model_class)

    def done(self):
        """
        Always call this upon completion to make sure the final partial chunk
        is saved.
        """
        for model_name, objs in self._create_queues.items():
            if len(objs) > 0:
                self._commit(apps.get_model(model_name))

def file_handler2(filename,allocation):
    data = pd.read_excel(filename)
    errors = []
    if not data.isnull().values.any():
        if not data['BIRTH CERTIFICATE NUMBER'].duplicated().any():
            if data.loc[:,'AMOUNT'].sum() < allocation:
                return errors,data
            else:
                errors.append('Amount disbursed is more than the amount allocated!')
        else:
            errors.append('There are duplicate Birth Certificate Numbers!')
    else:
        errors.append('There are empty cells in the document! Make sure all data is entered for each student')
    return errors,None

def file_creator(applications,school,year):
    data = {}
    a = 0
    data['NAME'] = []
    data['ADMISSION/REGISTRATION'] = []
    data['GENDER'] = []
    data['AMOUNT'] = []
    for application in applications:
        data['NAME'].append(application.full_name)
        data['ADMISSION/REGISTRATION'].append(application.admission_no)
        data['GENDER'].append('Male' if application.gender == 'm' else 'Female')
        data['AMOUNT'].append(application.amount)

        a += 1
    df = pd.DataFrame(data)
    year = year.replace('/',':')
    df.to_excel(f'media/{year}-{school}-Students List.xlsx')

def file_creator2(applications,filter,year):
    data = {}
    a = 0
    data['NAME'] = []
    data['ADMISSION/REGISTRATION'] = []
    data['BIRTH CERTIFICATE NUMBER'] = []
    data['WARD'] = []
    data['GENDER'] = []
    data['INSTITUTION'] = []
    data['BANK'] = []
    data['ACCOUNT'] = []
    data['BRANCH'] = []
    data['AMOUNT'] = []
    for application in applications:
        data['NAME'].append(application.full_name)
        data['ADMISSION/REGISTRATION'].append(application.admission_no)
        data['GENDER'].append('Male' if application.gender == 'm' else 'Female')
        data['AMOUNT'].append(application.amount)
        data['WARD'].append(application.ward.name)
        data['INSTITUTION'].append(application.institution)
        data['BANK'].append(application.bank)
        data['ACCOUNT'].append(application.account)
        data['BRANCH'].append(application.branch)
        data['BIRTH CERTIFICATE NUMBER'].append(application.birth_cert_no)

        a += 1
    df = pd.DataFrame(data)
    year = year.replace('/',':')
    df.to_excel(f'media/{year}-{filter}-Students List.xlsx')
    return f'media/{year}-{filter}-Students List.xlsx'


""" def file_creator(applications):
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
    
    wb.save('Students List.xlsx') """