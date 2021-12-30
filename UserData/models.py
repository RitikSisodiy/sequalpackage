from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from package.models import package, test



class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
class Booking(models.Model):
    choices=(
        ("package","package"),
        ("test","test")
    )
    Booking_id = models.CharField(max_length=50,blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="Booking")
    type = models.CharField(max_length=10,choices=choices)
    test = models.ForeignKey(test,on_delete=models.SET_NULL,null=True,blank=True)
    package = models.ForeignKey(package,on_delete=models.SET_NULL,null=True,blank=True)
    def clean(self) -> None:
        if self.type == "package" and not self.package:
            raise ValidationError(
                {'package': 'please select the package'}
            )
        if self.type == "test" and not self.test:
            raise ValidationError(
                {'test': 'please select the test'}
            )
    def save(self,*args, **kwargs):
        if self.type == "package":
            self.test = None
        if self.type == "test":
            self.package = None
        super(Booking, self).save(*args, **kwargs)
        self.Booking_id = f"booking{self.id}"
        super(Booking, self).save(*args, **kwargs)
    def __str__(self):
        return self.Booking_id

class report(models.Model):
    booking = models.OneToOneField(Booking,on_delete=models.CASCADE,related_name="report")
    report = models.FileField(upload_to="reports",validators=[FileExtensionValidator( ['pdf','tif','jpg','jpeg','gif','png','docx'] ) ],)
    message = models.TextField(blank=True)
    def clean(self, *args, **kwargs):
        print(type(self.report.size))
        if self.report.size > (1*1024*1024):
            raise ValidationError({'report':'Report size should be less than 5mb'})