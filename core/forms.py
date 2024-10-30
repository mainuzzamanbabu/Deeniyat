from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DailyTask, Donation

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class DailyTaskForm(forms.ModelForm):
    class Meta:
        model = DailyTask
        fields = ['date', 'salat_status', 'quran_reading']

class DonationVerificationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = ['transaction_id', 'amount']
