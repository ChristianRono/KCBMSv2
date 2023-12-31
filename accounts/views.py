import os
import mimetypes
import pandas as pd

from django.shortcuts import render,redirect,HttpResponse
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.mail import EmailMessage

from master.models import Application,FinancialYear
from accounts.forms import EmailForm

from main.utility import file_creator,file_creator2

# Create your views here.

def homepage(request):
    total_all_applications = Application.objects.all().count()
    total_current_applications = Application.objects.filter(financial_year__is_active=True).count()
    all_wards = Application.objects.values_list('ward__name',flat=True).distinct()
    current_wards = Application.objects.filter(financial_year__is_active=True).values_list('ward__name',flat=True).distinct()
    
    if total_all_applications > 0:
        # Do the statistics for all applications
        all_males = Application.objects.filter(gender='m').count()
        all_females = Application.objects.filter(gender='f').count()
        all_males_percentage = all_males / ( all_males + all_females ) * 100
        all_females_percentage = all_females / ( all_males + all_females ) * 100
        all_males_percentage = round(all_males_percentage,2)
        all_females_percentage = round(all_females_percentage,2)
    else:
        all_males = 0
        all_females = 0
        all_males_percentage = 0
        all_females_percentage = 0

    if total_current_applications > 0:
        # Do the statistics for current financial year applications
        current_males = Application.objects.filter(gender='m',financial_year__is_active=True).count()
        current_females = Application.objects.filter(gender='f',financial_year__is_active=True).count()
        current_males_percentage = current_males / ( current_males + current_females ) * 100
        current_females_percentage = current_females / ( current_males + current_females ) * 100
        current_males_percentage = round(current_males_percentage,2)
        current_females_percentage = round(current_females_percentage,2)
    else:
        current_males = 0
        current_females = 0
        current_males_percentage = 0
        current_females_percentage = 0

    ward_all_data = {}
    if total_all_applications > 0:
        for ward in all_wards:
            count = Application.objects.filter(ward__name=ward).count()
            ward_percentage = count / total_all_applications * 100
            ward_all_data[ward] = {"count":count,'percentage':round(ward_percentage,2)}
    
    ward_current_data = {}
    if total_current_applications > 0:
        for ward in current_wards:
            count = Application.objects.filter(ward__name=ward,financial_year__is_active=True).count()
            ward_percentage = count / total_current_applications * 100
            ward_current_data[ward] = {"count":count,'percentage':round(ward_percentage,2)}
    
    return render(request,"accounts_homepage.html",{"total_all_applications":total_all_applications,
                                                  "total_current_applications":total_current_applications,
                                                  "ward_current_data":ward_current_data,
                                                  "ward_all_data":ward_all_data,
                                                  "all_males":all_males,
                                                  "all_females":all_females,
                                                  "all_males_percentage":all_males_percentage,
                                                  "all_females_percentage":all_females_percentage,
                                                  "current_males":current_males,
                                                  "current_females":current_females,
                                                  "current_males_percentage":current_males_percentage,
                                                  "current_females_percentage":current_females_percentage})

def applications(request):
    financialyear = FinancialYear.objects.get(is_active=True)
    schools = Application.objects.values_list('institution', flat=True).distinct()
    banks = Application.objects.values_list('bank', flat=True).distinct()
    wards = Application.objects.values_list('ward__name', flat=True).distinct()
    applications = Application.objects.filter(financial_year=financialyear).order_by('full_name')
    paginator = Paginator(applications,10)
    page = request.GET.get('page')
    applications = paginator.get_page(page)
    count = Application.objects.filter(financial_year=financialyear).count()

    return render(request,"accounts_applications.html",{'applications':applications, 
                                                  'schools':schools, 
                                                  'wards':wards,
                                                  'banks':banks,
                                                  'count':count})

def list_filter(request):
    query = Q(financial_year__is_active=True)
    filter_q = 'Financial Year: Current'
    if 'school-checkbox' in request.POST:
        filter_q += ' & Institution:' + request.POST['school-dropdown']
        query = query & Q(institution=request.POST['school-dropdown'])
    if 'gender-checkbox' in request.POST:
        gender = "Male" if request.POST['gender-dropdown'] == 'm' else "Female"
        filter_q += ' & Gender:' + gender
        query = query & Q(gender=request.POST['gender-dropdown'])
    if 'bank-checkbox' in request.POST:
        filter_q += ' & Bank:' + request.POST['bank-dropdown']
        query = query & Q(bank=request.POST['bank-dropdown'])
    if 'ward-checkbox' in request.POST:
        filter_q += ' & Ward:' + request.POST['ward-dropdown']
        query = query & Q(ward__name=request.POST['ward-dropdown'])
    
    applications = Application.objects.filter(query)

    paginator = Paginator(applications,10)
    page = request.GET.get('page')
    applications = paginator.get_page(page)
    return render(request,"accounts_filter.html",{
        "applications":applications,
        "filter":filter_q})

def list_schools(request):
    schools = Application.objects.filter(financial_year__is_active=True).values_list('institution',flat=True).distinct()
    SCHOOLS = {}
    Total = 0
    for school in schools:
        applications = Application.objects.filter(institution=school,financial_year__is_active=True)
        sub_total = 0
        branch = {}
        account = {}
        for application in applications:
            sub_total += int(application.amount)
            b = branch.get(application.branch,0)
            branch[application.branch] = int(b) + 1
            a = account.get(application.account,0)
            account[application.account] = int(a) + 1
        
        if len(branch) > 3:
            branch = list(sorted(branch)[0:3])
            account = list(sorted(account)[0:3])
        else:
            branch = list(branch)
            account = list(account)
        SCHOOLS[application.institution] = {'bank':application.bank,'branch':branch,'account':account,'amount':sub_total}
        Total += sub_total
    return render(request,"accounts_schools.html",{'schools':SCHOOLS,'total':Total})

def list_students(request,institution):
    applications = Application.objects.filter(financial_year__is_active=True,institution=institution)

    paginator = Paginator(applications,10)
    page = request.GET.get('page')
    applications = paginator.get_page(page)
    return render(request,"accounts_students.html",{
        "applications":applications,'institution':institution})
    

def email(request,institution):
    if request.method == 'POST':
        form = EmailForm(request.POST,request.FILES)
        if form.is_valid():
            to = [form.cleaned_data['to']]
            re = form.cleaned_data['re']
            message = form.cleaned_data['message']
            doc = f"{FinancialYear.objects.get(is_active=True).name.replace('/',':')}-{institution}-Students List.xlsx"
            attachment = f'media/{doc}'
            email = EmailMessage(re,message,to=to)

            content = open(attachment, 'rb')
            email.attach(doc,content.read(),'application/pdf')
            email.send()
            os.remove(f'media/{doc}')
            return redirect("accounts homepage")
    else:
        applications = Application.objects.filter(institution=institution)
        year = FinancialYear.objects.get(is_active=True)
        file_creator(applications,institution,year.name)
        form =EmailForm({'re':'Bursary Students List','message':'This is an automatic message. Please do not reply.'})
        return render(request,"accounts_email.html",{'form':form,'institution':institution})
    
def download(request,filter):
    filters = filter.split('&')
    query = Q(financial_year__is_active=True)
    for filter in filters[1:]:
        parts = filter.split(':')
        part0 = parts[0].lower().strip()
        if part0 == 'ward':
            query = query & Q(ward__name=parts[1])
        else:
            query = query & Q((part0,parts[1]))
    applications = Application.objects.filter(query)
    applications.select_related('ward','financial_year')
    applications_list = list(applications.values('full_name',
                                                 'birth_cert_no',
                                                 'ward__name',
                                                 'gender',
                                                 'institution',
                                                 'bank',
                                                 'account',
                                                 'branch',
                                                 'amount',
                                                 'family_status',
                                                 'disability_status'))
    print(applications_list)
    year = FinancialYear.objects.get(is_active=True)
    df = pd.DataFrame(applications_list)
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{year}-{filter}.xlsx"'
    df.to_excel(response, index=False)
    return response
