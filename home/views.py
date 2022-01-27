
from django.shortcuts import redirect, render
from package.models import package
from .models import customer_contact,ContactInfo
from UserData.models import RequestedCallBack
from superuser.forms import GenForm
from django.contrib import messages
# Create your views here.
def index(request):
    res = {}
    res['packages'] = package.objects.all()
    res['bodyclass'] = "index-page"
    return render(request,'home/index.html',res)
def contact(request):
    res={}
    res['contactinfo'] = ContactInfo.objects.all()
    res["bodyclass"] = "contant-page"
    if request.method == 'POST':
        form = GenForm(customer_contact)
        form = form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Thanks for contacting us We will get back to you soon')
            return redirect('contact')
        else:
            for data in form.errors:
                messages.error(request,data)
    return render(request,'home/contact2.html',res)
def callback(request):
    form = GenForm(RequestedCallBack)
    if request.method == "POST":
        form = form(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Thanks for contacting us We will get back to you soon')
        else:
            for data in form.errors:
                messages.error(request,data)
        return redirect(request.GET['next'])
    return redirect('index')