from django.shortcuts import render,redirect
from django.core.paginator import Paginator
from django.db.models import Q,Count
from django.contrib import messages

from master.models import *
from master.forms import FinancialForm,AllocationForm

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
            ward_count = Application.objects.filter(ward__name=ward).count()
            ward_percentage = ward_count / total_all_applications * 100
            ward_female_count = Application.objects.filter(ward__name=ward,gender='f').count()
            female_percentage = ward_female_count / ward_count * 100
            ward_male_count = Application.objects.filter(ward__name=ward,gender='m').count()
            male_percentage = ward_male_count / ward_count * 100
            ward_pwd_count = Application.objects.filter(ward__name=ward,disability_status=True).count()
            pwd_percentage = ward_pwd_count / ward_count * 100
            ward_all_data[ward] = {
                "ward_count":ward_count,
                'ward_percentage':round(ward_percentage,2),
                'female_percentage':round(female_percentage,2),
                'male_percentage':round(male_percentage,2),
                'pwd_percentage':round(pwd_percentage,2)}
    
    ward_current_data = {}
    if total_current_applications > 0:
        for ward in current_wards:
            ward_count = Application.objects.filter(ward__name=ward,financial_year__is_active=True).count()
            ward_percentage = ward_count / total_all_applications * 100
            ward_female_count = Application.objects.filter(ward__name=ward,gender='f',financial_year__is_active=True).count()
            female_percentage = ward_female_count / ward_count * 100
            ward_male_count = Application.objects.filter(ward__name=ward,gender='m',financial_year__is_active=True).count()
            male_percentage = ward_male_count / ward_count * 100
            ward_pwd_count = Application.objects.filter(ward__name=ward,disability_status=True,financial_year__is_active=True).count()
            pwd_percentage = ward_pwd_count / ward_count * 100
            ward_current_data[ward] = {
                "ward_count":ward_count,
                'ward_percentage':round(ward_percentage,2),
                'female_percentage':round(female_percentage,2),
                'male_percentage':round(male_percentage,2),
                'pwd_percentage':round(pwd_percentage,2)}
    
    return render(request,"master_homepage.html",{"total_all_applications":total_all_applications,
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

def allocations(request):
    allocations = Allocation.objects.all()
    return render(request,"master_allocations.html",{"allocations":allocations})

def allocations_new(request):
    if request.method == 'POST':
        form = AllocationForm(request.POST)
        if form.is_valid():
            ward = form.cleaned_data['ward']
            financial_year = form.cleaned_data['financial_year']
            amount = form.cleaned_data['amount']
            allocation = Allocation.objects.create(ward=ward,financial_year=financial_year,amount=amount)
            allocation.save()
            return redirect('master allocations')
    else:
        form = AllocationForm()
        return render(request,"master_allocations_form.html",{'form':form})

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

    return render(request,"master_applications.html",{'applications':applications, 
                                                  'schools':schools, 
                                                  'wards':wards,
                                                  'banks':banks,
                                                  'count':count})

def list_filter(request):
    query = Q(financial_year__is_active=True)
    filter_q = 'Financial Year: Current'
    if 'school-checkbox' in request.POST:
        filter_q += ' & School:' + request.POST['school-dropdown']
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
    return render(request,"master_applications_filter.html",{
        "applications":applications,
        "filter":filter_q})

def users(reqeust):
    edu_admin_users = KCBMSUser.objects.filter(is_edu_admin=True)
    accountant_users = KCBMSUser.objects.filter(is_accountant=True)
    ward_admin_users = KCBMSUser.objects.filter(is_ward_admin=True)
    return render(reqeust,"master_users.html",{
        "edu_admin_users":edu_admin_users,
        "accountant_users":accountant_users,
        "ward_admin_users":ward_admin_users})

def activate_user(request,id):
    user = User.objects.get(id=id)
    user.is_active = True
    user.save()
    return redirect('master users')

def deactivate_user(request,id):
    user = User.objects.get(id=id)
    user.is_active = False
    user.save()
    return redirect('master users')

def financial(request):
    financials = FinancialYear.objects.all()
    return render(request,"master_financial.html",{"financials":financials})

def financial_new(request):
    if request.method == 'POST':
        form = FinancialForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            is_active = form.cleaned_data['is_active']
            if is_active:
                financial_year = FinancialYear.objects.get(is_active=True)
                financial_year.is_active = False
                financial_year.save()
                financial_year = FinancialYear.objects.create(name=name,is_active=is_active)
                financial_year.save()
            else:
                financial_year = FinancialYear.objects.create(name=name,is_active=is_active)
                financial_year.save()
            return redirect('master financial')
    else:
        form = FinancialForm()
        return render(request,'master_financial_form.html',{'form':form})

def financial_deactivate(request,id):
    financial_year = FinancialYear.objects.get(id=id)
    financial_year.is_active = False
    financial_year.save()
    return redirect('master financial')

def financial_activate(request,id):
    try:
        financial_year = FinancialYear.objects.get(is_active=True)
        financial_year.is_active = False
        financial_year.save()
    except:
        pass
    financial_year = FinancialYear.objects.get(id=id)
    financial_year.is_active = True
    financial_year.save()
    return redirect('master financial')

def check_applications(request):
    dups = (
        Application.objects.values('birth_cert_no')
        .annotate(count=Count('id'))
        .values('birth_cert_no')
        .order_by()
        .filter(count__gt=1)
    )
    applications = Application.objects.filter(birth_cert_no__in=dups)
    if applications.exists():
        return render(request,'master_applications_check.html',{'applications':applications})
    else:
        messages.info(request,'No duplicate Birth Certificates found!')
        return redirect('master applications')