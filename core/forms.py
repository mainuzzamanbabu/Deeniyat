from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DailyTask, Donation

# class UserRegistrationForm(UserCreationForm):
#     email = forms.EmailField(required=True)
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control form-control-lg'}),
        }

class DailyTaskForm(forms.ModelForm):
    class Meta:
        model = DailyTask
        fields = ['date', 'salat_status', 'quran_reading']

class DonationVerificationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['transaction_id', 'amount']
