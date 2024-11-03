from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

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

class DonationSummary(models.Model):
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    donation_count = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Total Donations: {self.total_amount} - Count: {self.donation_count}"

@receiver(post_save, sender=Donation)
def update_donation_summary_on_save(sender, instance, created, **kwargs):
    summary, _ = DonationSummary.objects.get_or_create(id=1)

    if created:
        if instance.verified:
            summary.total_amount += instance.amount
            summary.donation_count += 1
            summary.save()
    else:
        previous_instance = Donation.objects.get(id=instance.id)
        if not previous_instance.verified and instance.verified:
            summary.total_amount += instance.amount
            summary.donation_count += 1
            summary.save()
        elif previous_instance.verified and not instance.verified:
            summary.total_amount -= instance.amount
            summary.donation_count -= 1
            summary.save()

@receiver(post_delete, sender=Donation)
def update_donation_summary_on_delete(sender, instance, **kwargs):
    summary, _ = DonationSummary.objects.get_or_create(id=1)

    # Recalculate total and count after deletion
    summary.total_amount = Donation.objects.filter(verified=True).aggregate(total=Sum('amount'))['total'] or 0
    summary.donation_count = Donation.objects.filter(verified=True).count()
    summary.save()