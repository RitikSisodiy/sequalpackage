# Generated by Django 4.0 on 2022-01-04 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserData', '0005_alter_report_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='content_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
