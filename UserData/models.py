from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from package.models import package, test
from django.urls import reverse
from package.models import get_random_string
def gen_username(length):
    username= get_random_string(length)
    userdata = User.objects.filter(username=username)
    if userdata.exists():
        return gen_username(length)
    return username

class User(AbstractUser):
    phone = models.CharField(max_length=10)
    gender = models.CharField(max_length=5,blank=True,null=True)
    dob = models.DateField(blank=True,null=True)

    def save(self,*args, **kwargs):
        if self.id is None:
            check = User.objects.filter(phone= self.phone)
            if len(self.phone)!=10:
                raise ValidationError("invalid phone")
            if check.exists():
                raise ValidationError("This phone is already exist")
            self.username = gen_username(8)
        super(User, self).save(*args, **kwargs)

class TempUser(models.Model):
    phone = models.CharField(max_length=13)
    otp = models.CharField(max_length=8)
    expire = models.DateTimeField()


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
    content_type = models.CharField(null=True, blank=True, max_length=100)

    def save(self, *args, **kwargs):
        try:
            self.content_type = self.report.file.content_type
        except:
            pass
        super().save(*args, **kwargs)
    def clean(self, *args, **kwargs):
        print(type(self.report.size))
        if self.report.size > (5*1024*1024):
            raise ValidationError({'report':'Report size should be less than 5mb'})
    def BulkOprationButton(self):
        data = (
            # ("button name","button class","funtionname","reversed url","redirection:boolan")
            ("Send Report",'btn btn-warning',"HandleSendReport",reverse('bulksendmail'),False),
            ("Bluk Report upload",'btn btn-secondary',"HandleUploadReport",reverse('bulkreportupload'),True),
        )
        return data