from django import forms

class EmailForm(forms.Form):
    to = forms.EmailField()
    re = forms.CharField()
    message = forms.CharField(widget=forms.Textarea())
