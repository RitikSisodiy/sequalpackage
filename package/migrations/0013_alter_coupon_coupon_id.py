# Generated by Django 4.0 on 2021-12-29 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0012_alter_coupon_coupon_issed_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='Coupon_id',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
