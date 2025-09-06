from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import EmployerProfile

class EmployerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    company_name = forms.CharField(max_length=255)
    website = forms.URLField(required=False)
    location = forms.CharField(max_length=255, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','email','first_name','last_name','password1','password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = 'employer'
        if commit:
            user.save()
            # create employer profile
            EmployerProfile.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                website=self.cleaned_data.get('website',''),
                location=self.cleaned_data.get('location',''),
            )
        return user
    
class JobSeekerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','email','first_name','last_name','password1','password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.role = 'jobseeker'
        if commit:
            user.save()
        return user

