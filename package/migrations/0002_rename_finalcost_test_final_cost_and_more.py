# Generated by Django 4.0 on 2021-12-28 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='test',
            old_name='finalCost',
            new_name='final_cost',
        ),
        migrations.RenameField(
            model_name='test',
            old_name='sampleColllectionCharges',
            new_name='sample_colllection_charges',
        ),
        migrations.RenameField(
            model_name='test',
            old_name='testDescription',
            new_name='test_description',
        ),
        migrations.RenameField(
            model_name='test',
            old_name='testName',
            new_name='test_name',
        ),
        migrations.RenameField(
            model_name='test',
            old_name='testPrice',
            new_name='test_price',
        ),
        migrations.RenameField(
            model_name='test',
            old_name='testUniqueId',
            new_name='test_uniqueId',
        ),
        migrations.AlterField(
            model_name='test',
            name='dicount',
            field=models.FloatField(help_text='You Can Ammount or Percent of Ammount Eg: 100 or 10%'),
        ),
    ]
