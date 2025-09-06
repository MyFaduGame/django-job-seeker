from django import forms
from .models import Job, Application

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title','description','category','location','salary_min','salary_max','employment_type','is_active','expires_at']

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume','cover_letter']
