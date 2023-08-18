from django import forms
from master.models import FinancialYear,Allocation

class FinancialForm(forms.ModelForm):
    class Meta:
        model = FinancialYear
        fields = ['name','is_active']

class AllocationForm(forms.ModelForm):
    class Meta:
        model = Allocation
        fields = ['ward','financial_year','amount']