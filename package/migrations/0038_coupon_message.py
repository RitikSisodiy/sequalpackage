# Generated by Django 4.0 on 2022-02-09 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0037_tempbooking_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='message',
            field=models.CharField(default='Applied', help_text='User will see this messge when he/she apply the coupen', max_length=100),
        ),
    ]
