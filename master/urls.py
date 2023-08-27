from django.urls import path
from master.views import (
    homepage,
    list_filter,
    applications,
    users,
    activate_user,
    deactivate_user,
    financial,
    allocations,
    allocations_new,
    financial_activate,
    financial_deactivate,
    financial_new,
    check_applications
    )

urlpatterns = [
    path('applications/',view=applications,name='master applications'),
    path('users/',view=users,name='master users'),
    path('users/activate/<int:id>/',view=activate_user,name='master users activate'),
    path('users/deactivate/<int:id>/',view=deactivate_user,name='master users deactivate'),
    path('financial/',view=financial,name='master financial'),
    path('allocations/',view=allocations,name='master allocations'),
    path('allocations/new/',view=allocations_new,name='master allocations form'),
    path('filter/',view=list_filter, name="master filter"),
    path('financial/new/',view=financial_new,name="master financial form"),
    path('financial/deactivate/<int:id>/',view=financial_deactivate,name='master financial deactivate'),
    path('financial/activate/<int:id>/',view=financial_activate,name='master financial activate'),
    path('check/',view=check_applications,name='check applications'),
    path('',view=homepage,name='master homepage'),
]