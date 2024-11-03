from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserRegistrationForm, DailyTaskForm, DonationVerificationForm
from .models import DailyTask, Donation, DonationSummary
from django.contrib.auth.models import User  # Import the User model
from django.db.models import Sum
from django.contrib.auth.models import Group

from datetime import datetime

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

# @login_required
# @user_passes_test(is_superuser_or_accounts)
# def approve_donation(request):
#     donations = Donation.objects.filter(verified=False)
#     if request.method == "POST":
#         donation_id = request.POST.get("donation_id")
#         donation = Donation.objects.get(id=donation_id)
#         donation.verified = True
#         donation.verified_by = request.user
#         donation.save()
#         return redirect("accounts_admin_dashboard")
#     return render(request, "accounts_admin_dashboard.html", {"donations": donations})


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

@require_POST
@login_required
@user_passes_test(is_superuser_or_accounts)
def edit_donation_accounts(request):
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
    
    return redirect("accounts_admin_dashboard")

# @login_required
# @user_passes_test(lambda u: u.groups.filter(name='accounts').exists() or u.is_superuser)
# def accounts_admin_dashboard(request):
#     all_data = {
#         'users': User.objects.all(),
#         'tasks': DailyTask.objects.all(),
#         'donations': Donation.objects.all(),
#     }
#     return render(request, 'accounts_admin_dashboard.html', all_data)
@login_required
@user_passes_test(lambda u: u.groups.filter(name='accounts').exists() or u.is_superuser)
def accounts_admin_dashboard(request):
    # Get all donations initially
    donations = Donation.objects.all()
    print("ddd",donations)
    # Get filter parameters from request
    user_filter = request.GET.get('user')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    payment_month = request.GET.get('payment_month')
    status = request.GET.get('status')
    min_amount = request.GET.get('min_amount')
    max_amount = request.GET.get('max_amount')

    # Apply filters
    if user_filter:
        donations = donations.filter(user__username__icontains=user_filter)
    
    if date_from:
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
            donations = donations.filter(payment_date__gte=date_from)
        except ValueError:
            pass

    if date_to:
        try:
            date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
            donations = donations.filter(payment_date__lte=date_to)
        except ValueError:
            pass
    
    if payment_month and payment_month != 'all':
        donations = donations.filter(payment_month=payment_month)

    if status and status != 'all':
        donations = donations.filter(verified=(status == 'verified'))

    if min_amount:
        try:
            donations = donations.filter(amount__gte=float(min_amount))
        except ValueError:
            pass

    if max_amount:
        try:
            donations = donations.filter(amount__lte=float(max_amount))
        except ValueError:
            pass
    donation_summary = DonationSummary.objects.first()
    total_donations = donation_summary.total_amount if donation_summary else 0
    donation_count = donation_summary.donation_count if donation_summary else 0
    context = {
        'donations': donations,
        'users': User.objects.all(),
        'tasks': DailyTask.objects.all(),
        'months_choices': Donation.MONTH_CHOICES,
        'total_donations': total_donations,
        'donation_count': donation_count,

        # Add current filter values to context for form persistence
        'current_filters': {
            'user': user_filter or '',
            'date_from': date_from or '',
            'date_to': date_to or '',
            'payment_month': payment_month or 'all',
            'status': status or 'all',
            'min_amount': min_amount or '',
            'max_amount': max_amount or '',
        }
    }
    
    return render(request, 'accounts_admin_dashboard.html', context)

# @login_required
# @user_passes_test(lambda u: u.groups.filter(name='accounts').exists() or u.is_superuser)
# def accounts_admin_dashboard(request):
#     donations = Donation.objects.all()
    
#     # Get the donation summary (assume a single record with id=1 exists)
#     donation_summary = DonationSummary.objects.first()
#     total_donations = donation_summary.total_amount if donation_summary else 0
#     donation_count = donation_summary.donation_count if donation_summary else 0

#     context = {
#         'donations': donations,
#         'total_donations': total_donations,
#         'donation_count': donation_count,
#         # Other context data
#     }
#     return render(request, 'accounts_admin_dashboard.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser or u.groups.filter(name='accounts').exists())
def approve_donation(request):
    donations = Donation.objects.filter(verified=False)
    
    if request.method == "POST":
        donation_id = request.POST.get("donation_id")
        donation = get_object_or_404(Donation, id=donation_id)
        
        if not donation.verified:
            # Mark the donation as verified
            donation.verified = True
            donation.verified_by = request.user
            donation.save()

            # Update DonationSummary
            summary, created = DonationSummary.objects.get_or_create(id=1)
            summary.total_amount += donation.amount
            summary.donation_count += 1
            summary.save()

            messages.success(request, "Donation approved and summary updated.")
        else:
            messages.warning(request, "Donation is already verified.")

        return redirect("accounts_admin_dashboard")
    
    return render(request, "approve_donation.html", {"donations": donations})