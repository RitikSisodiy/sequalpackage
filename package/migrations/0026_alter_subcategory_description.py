# Generated by Django 4.0 on 2022-01-27 09:38

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('package', '0025_subcategory_description_subcategory_shortdes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategory',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True),
        ),
    ]
