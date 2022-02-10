# Generated by Django 4.0 on 2022-02-10 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserData', '0028_alter_booking_status'),
        ('package', '0040_remove_tempbooking_bookingid_tempbooking_bookingid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tempbooking',
            name='bookingid',
        ),
        migrations.AddField(
            model_name='tempbooking',
            name='bookingid',
            field=models.ManyToManyField(null=True, related_name='Transtaction', to='UserData.Booking'),
        ),
    ]
