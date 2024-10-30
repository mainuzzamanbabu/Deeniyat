from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class DailyTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    date = models.DateField(default=timezone.now)
    salat_status = models.CharField(max_length=10, choices=[("Jamat", "Jamat"), ("Alone", "Alone"), ("Kazah", "Kazah")])
    quran_reading = models.CharField(max_length=50, choices=[("Yes", "Yes"), ("No", "No"), ("Unable", "I don't able to read Quran")])

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="donations")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=50)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="verified_donations")
