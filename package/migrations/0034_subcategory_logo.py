# Generated by Django 4.0 on 2022-01-28 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0033_alter_package_package_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subcategory',
            name='logo',
            field=models.ImageField(default='logos/logo.png', upload_to='logos'),
        ),
    ]
