# Generated by Django 4.0 on 2022-01-27 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0029_package_publish'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='test_category',
            field=models.ManyToManyField(blank=True, null=True, related_name='test', to='package.Subcategory'),
        ),
    ]
