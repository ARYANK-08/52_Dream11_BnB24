from django import forms
from .models import PatientProfile, PatientReport

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = PatientProfile
        fields = ['name', 'last_name', 'age', 'gender', 'location', 'diseases', 'phone_number']

    def __init__(self, *args, **kwargs):
        super(PatientProfileForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your name'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your last name'})
        self.fields['age'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your age'})
        self.fields['gender'].widget.attrs.update({'class': 'form-select'})
        self.fields['location'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your location'})
        self.fields['diseases'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter any diseases you have'})
        self.fields['phone_number'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Enter your phone number'})


class PatientReportForm(forms.ModelForm):
    class Meta:
        model = PatientReport
        fields = ['user', 'dr_name', 'disease', 'precaution', 'medication']