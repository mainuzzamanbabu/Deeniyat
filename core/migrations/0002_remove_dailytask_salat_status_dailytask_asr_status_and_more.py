# Generated by Django 5.1.2 on 2024-11-02 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailytask',
            name='salat_status',
        ),
        migrations.AddField(
            model_name='dailytask',
            name='asr_status',
            field=models.CharField(choices=[('Jamat', 'Jamat'), ('Alone', 'Alone'), ('Kazah', 'Kazah')], default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dailytask',
            name='dhuhr_status',
            field=models.CharField(choices=[('Jamat', 'Jamat'), ('Alone', 'Alone'), ('Kazah', 'Kazah')], default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dailytask',
            name='fajr_status',
            field=models.CharField(choices=[('Jamat', 'Jamat'), ('Alone', 'Alone'), ('Kazah', 'Kazah')], default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dailytask',
            name='isha_status',
            field=models.CharField(choices=[('Jamat', 'Jamat'), ('Alone', 'Alone'), ('Kazah', 'Kazah')], default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dailytask',
            name='maghrib_status',
            field=models.CharField(choices=[('Jamat', 'Jamat'), ('Alone', 'Alone'), ('Kazah', 'Kazah')], default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dailytask',
            name='masnoon_amol',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='dailytask',
            name='reading_hadith',
            field=models.BooleanField(default=False),
        ),
    ]
