from django import forms

class ApplicationForm(forms.Form):
    file_name = forms.FileField()