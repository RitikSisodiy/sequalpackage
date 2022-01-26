from email import message
from statistics import mode
from django.db import models

# Create your models here.
class ContactInfo(models.Model):
    companyname = models.CharField(max_length=100)
    phone = models.CharField(max_length=13)
    helpline = models.CharField(max_length=16)
    address = models.TextField()
    def __str__(self) -> str:
        return self.companyname
class contactMails(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    def __str__(self) -> str:
        return self.email
class customer_contact(models.Model):
    name= models.CharField(max_length=100)
    email= models.CharField(max_length=100)
    mobile= models.CharField(max_length=13)
    company= models.CharField(max_length=100)
    message= models.TextField(max_length=100)
    def __str__(self) -> str:
        return self.name