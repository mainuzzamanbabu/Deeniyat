from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DailyTask, Donation


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

# class DailyTaskForm(forms.ModelForm):
#     class Meta:
#         model = DailyTask
#         fields = ['date', 'salat_status', 'quran_reading']
class DailyTaskForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control form-control-lg', 'type': 'date'}))
    
    class Meta:
        model = DailyTask
        fields = [
            'date',
            'fajr_status', 'dhuhr_status', 'asr_status', 'maghrib_status', 'isha_status',
            'quran_reading',
            'masnoon_amol',
            'reading_hadith',
        ]
        widgets = {
            'fajr_status': forms.Select(attrs={'class': 'form-control'}),
            'dhuhr_status': forms.Select(attrs={'class': 'form-control'}),
            'asr_status': forms.Select(attrs={'class': 'form-control'}),
            'maghrib_status': forms.Select(attrs={'class': 'form-control'}),
            'isha_status': forms.Select(attrs={'class': 'form-control'}),
            'quran_reading': forms.Select(attrs={'class': 'form-control'}),
            'masnoon_amol': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'reading_hadith': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
# forms.py
from django import forms
from .models import Donation

class DonationVerificationForm(forms.ModelForm):
    payment_date = forms.DateField(widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    payment_month = forms.ChoiceField(choices=Donation.MONTH_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Donation
        fields = ['transaction_id', 'amount', 'payment_date', 'payment_month']
        widgets = {
            'transaction_id': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }