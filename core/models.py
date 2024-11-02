from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# class DailyTask(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
#     date = models.DateField(default=timezone.now)
#     salat_status = models.CharField(max_length=10, choices=[("Jamat", "Jamat"), ("Alone", "Alone"), ("Kazah", "Kazah")])
#     quran_reading = models.CharField(max_length=50, choices=[("Yes", "Yes"), ("No", "No"), ("Unable", "I don't able to read Quran")])
class DailyTask(models.Model):
    SALAT_CHOICES = [
        ("Jamat", "Jamat"),
        ("Alone", "Alone"),
        ("Kazah", "Kazah"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    date = models.DateField(default=timezone.now)
    
    # Adding fields for each Salat
    fajr_status = models.CharField(max_length=10, choices=SALAT_CHOICES)
    dhuhr_status = models.CharField(max_length=10, choices=SALAT_CHOICES)
    asr_status = models.CharField(max_length=10, choices=SALAT_CHOICES)
    maghrib_status = models.CharField(max_length=10, choices=SALAT_CHOICES)
    isha_status = models.CharField(max_length=10, choices=SALAT_CHOICES)
    
    # Additional fields
    quran_reading = models.CharField(max_length=50, choices=[("Yes", "Yes"), ("No", "No"), ("Unable", "I don't able to read Quran")])
    masnoon_amol = models.BooleanField(default=False)
    reading_hadith = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.date}"

class Donation(models.Model):
    MONTH_CHOICES = [
        ('01', 'January'),
        ('02', 'February'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'),
        ('09', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="donations")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=50)
    verified = models.BooleanField(default=False)
    verified_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="verified_donations")
    payment_date = models.DateField(default=timezone.now)  # Field for payment date
    payment_month = models.CharField(max_length=2, choices=MONTH_CHOICES)  # Field for payment month selection

    def __str__(self):
        return f"Donation by {self.user.username} - {self.amount}"