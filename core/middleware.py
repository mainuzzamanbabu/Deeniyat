# middleware.py
from django.db.models import Sum
from .models import Donation

class TotalDonationsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Calculate total donations only if the user is authenticated
        if request.user.is_authenticated:
            total_donations = Donation.objects.filter(user=request.user).aggregate(Sum('amount'))['amount__sum'] or 0
            request.total_donations = total_donations
        else:
            request.total_donations = 0

        response = self.get_response(request)
        return response
