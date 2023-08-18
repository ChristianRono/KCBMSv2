from django.contrib import admin
from master.models import FinancialYear,Ward,Allocation,Profile,Application

# Register your models here.
admin.site.register(FinancialYear)
admin.site.register(Ward)
admin.site.register(Allocation)
admin.site.register(Profile)
admin.site.register(Application)