from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserRegistrationForm, DailyTaskForm, DonationVerificationForm
from .models import DailyTask, Donation
from django.contrib.auth.models import User  # Import the User model
from django.db.models import Sum
from django.contrib.auth.models import Group


def donation_total(request):
    if request.user.is_authenticated:
        total_donations = Donation.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
    else:
        total_donations = 0
    return {'total_donations': total_donations}
def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        print(form)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "There was an error in the form. Please correct it.")
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

from django.contrib import messages

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
            if user is not None:
                login(request, user)
                return redirect('dashboard')
        else:
            messages.error(request, "Your username or password is incorrect")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')
@login_required
def dashboard(request):
    tasks = DailyTask.objects.filter(user=request.user)
    print(tasks)
    donations = Donation.objects.filter(user=request.user)
    total_donations = donations.aggregate(Sum('amount'))['amount__sum'] or 0
    print(total_donations)
    return render(request, 'dashboard.html', {
        'tasks': tasks,
        'donations': donations,
        'total_donations': total_donations
    })

@login_required
def submit_daily_task(request):
    if request.method == "POST":
        form = DailyTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = DailyTaskForm()
    return render(request, 'submit_daily_task.html', {'form': form})

@login_required
def submit_donation_verification(request):
    if request.method == "POST":
        form = DonationVerificationForm(request.POST)
        if form.is_valid():
            donation = form.save(commit=False)
            donation.user = request.user
            donation.save()
            return redirect('dashboard')
    else:
        form = DonationVerificationForm()
    return render(request, 'submit_donation_verification.html', {'form': form})
# @login_required
# def approve_donation(request):
#     donations = Donation.objects.filter(verified=False)
#     return render(request, 'approve_donation.html', {'donations': donations})

@login_required
def superadmin_dashboard(request):
    all_data = {
        'users': User.objects.all(),
        'tasks': DailyTask.objects.all(),
        'donations': Donation.objects.all(),
    }
    return render(request, 'superadmin_dashboard.html', all_data)




def is_superuser_or_accounts(user):
    return user.is_superuser or user.groups.filter(name='accounts').exists()

@login_required
@user_passes_test(is_superuser_or_accounts)
def approve_donation(request):
    donations = Donation.objects.filter(verified=False)
    if request.method == "POST":
        donation_id = request.POST.get("donation_id")
        donation = Donation.objects.get(id=donation_id)
        donation.verified = True
        donation.verified_by = request.user
        donation.save()
        return redirect("approve_donation")
    return render(request, "approve_donation.html", {"donations": donations})


from django.views.decorators.http import require_POST

@require_POST
@login_required
@user_passes_test(is_superuser_or_accounts)
def edit_donation(request):
    donation_id = request.POST.get("donation_id")
    amount = request.POST.get("amount")
    transaction_id = request.POST.get("transaction_id")
    
    try:
        donation = Donation.objects.get(id=donation_id)
        donation.amount = amount
        donation.transaction_id = transaction_id
        donation.save()
        messages.success(request, "Donation updated successfully.")
    except Donation.DoesNotExist:
        messages.error(request, "Donation not found.")
    
    return redirect("approve_donation")

@login_required
@user_passes_test(lambda u: u.groups.filter(name='accounts').exists() or u.is_superuser)
def accounts_admin_dashboard(request):
    all_data = {
        'users': User.objects.all(),
        'tasks': DailyTask.objects.all(),
        'donations': Donation.objects.all(),
    }
    return render(request, 'accounts_admin_dashboard.html', all_data)
