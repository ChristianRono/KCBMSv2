from django.urls import path
from accounts.views import homepage,applications,list_filter,list_schools,list_students,email,download

urlpatterns = [
    path('applications/',view=applications,name='accounts applications'),
    path('filter/',view=list_filter,name='accounts filter'),
    path('schools/',view=list_schools,name='accounts schools'),
    path('students/<str:institution>/',view=list_students,name='accounts students'),
    path('email/<str:institution>/',view=email,name='accounts email'),
    path('download/<str:filter>/',view=download,name="accounts download"),
    path('',view=homepage,name='accounts homepage'),
]