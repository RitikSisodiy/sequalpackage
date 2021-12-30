from django.db import models

from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
class aboutContact(models.Model):
    logo = models.ImageField(upload_to="logo")
    AdminTitle = models.CharField(max_length=30)
    favicon  = models.ImageField(upload_to='logo')
    