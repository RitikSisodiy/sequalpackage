# Generated by Django 4.0 on 2021-12-28 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0004_alter_test_disount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='final_cost',
            field=models.FloatField(blank=True, max_length=50),
        ),
    ]
