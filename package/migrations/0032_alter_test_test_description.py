# Generated by Django 4.0 on 2022-01-27 11:32

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0031_test_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='test_description',
            field=ckeditor_uploader.fields.RichTextUploadingField(),
        ),
    ]
