from django.contrib import admin

from core.models import DailyTask, Donation

# Register your models here.
admin.site.register(DailyTask)
admin.site.register(Donation)