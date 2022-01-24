from django.shortcuts import render
from .models import package
# Create your views here.
def packagedetails(request,slug):
    res = {}
    res['package'] = package.objects.get(slug=slug)
    totaltest = 0
    for data in res['package'].Porfile_collection.all():
        totaltest += data.Select_Test_id.all().count()
    res['totaltest'] = totaltest
    return render(request,'package/packageDetails.html',res)
def booknow(request,slug):
    return render(request,'package/booknow.html')