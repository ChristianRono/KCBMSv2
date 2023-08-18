from django.urls import path
from main.views import homepage

urlpatterns = [
    path('',view=homepage,name='main homepage'),
]