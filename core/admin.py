from django.contrib import admin

from core.models import DailyTask, Donation, DonationSummary

# Register your models here.
admin.site.register(DailyTask)
admin.site.register(Donation)
admin.site.register(DonationSummary)
from .models import Constitution

admin.site.register(Constitution)