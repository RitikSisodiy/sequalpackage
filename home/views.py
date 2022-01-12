from django.shortcuts import render
from package.models import package
# Create your views here.
def index(request):
    res = {}
    res['packages'] = package.objects.all()
    res['bodyclass'] = "index-page"
    return render(request,'home/index.html',res)