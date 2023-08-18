from django.shortcuts import render,redirect
from main.forms import ApplicationForm

from main.utility import file_handler
# Create your views here.
def homepage(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST,request.FILES)
        if form.is_valid():
            file_name = request.FILES['file_name']
            status,message =file_handler(file_name)
            if status:
                form = ApplicationForm()
                return render(request,'main_homepage.html',{"form":form,'status':status})
            else:
                form = ApplicationForm()
                return render(request,'main_homepage.html',{"form":form,'status':status})
    else:
        form = ApplicationForm()
        return render(request,'main_homepage.html',{"form":form,"status":None})