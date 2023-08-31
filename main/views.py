from django.shortcuts import render,redirect
from main.forms import ApplicationForm

from main.utility import file_handler2,BulkCreateManager
from master.models import Allocation,Ward,Application,FinancialYear

# Create your views here.
def homepage(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST,request.FILES)
        if form.is_valid():
            file_name = request.FILES['file_name']
            ward = Ward.objects.get(name='Ainamoi')
            allocation = Allocation.objects.get(financial_year__is_active=True,ward=ward)
            errors,datas =file_handler2(file_name,allocation.amount)
            if not errors:
                length = datas.count()[0]
                DATA = datas.to_dict()
                bulk_mgr = BulkCreateManager(chunk_size=20)
                for i in range(length):
                    fs = ''
                    ss = ''

                    if DATA['SCHOOL TYPE'] == 'Secondary':
                        ss = 's'
                    elif DATA['SCHOOL TYPE'] == 'Tertiary':
                        ss = 't'
                    else:
                        ss = 'p'

                    if DATA['FAMILY STATUS'][i] == 'Both Parents':
                        fs = 'b'
                    elif DATA['FAMILY STATUS'][i] == 'Single Parents':
                        fs = 's'
                    else:
                        fs = 'o'

                    bulk_mgr.add(Application(
                        birth_cert_no = DATA["BIRTH CERTIFICATE NUMBER"][i],
                        full_name = DATA["NAME"][i],
                        admission_no = DATA["ADMISSION/REGISTRATION"][i],
                        ward = Ward.objects.get_or_create(name=DATA["WARD"][i])[0],
                        gender = 'm' if DATA["GENDER"][i] == 'Male' else 'f',
                        institution = DATA["INSTITUTION"][i],
                        bank = DATA["BANK"][i],
                        account = DATA["ACCOUNT"][i],
                        family_status = fs,
                        school_type = ss,
                        branch = DATA['BRANCH'][i],
                        disability_status = True if DATA["DISABILITY STATUS"][i] == 1 else False,
                        amount = DATA["AMOUNT"][i],
                        financial_year = FinancialYear.objects.get(is_active=True),
                    ))
                    #application.save()
                return render(request,'main_homepage.html',{"form":form,'errors':errors,'success':True})
            else:
                form = ApplicationForm()
                return render(request,'main_homepage.html',{"form":form,'errors':errors})
    else:
        form = ApplicationForm()
        return render(request,'main_homepage.html',{"form":form,"status":None})