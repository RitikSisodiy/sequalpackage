from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import JsonResponse
from UserData.models import Family
from superuser.forms import GenForm

def dashboard(request):
    res={}
    res['bodyclass'] = "dashboard"
    return render(request,'UserData/user/dashboard.html',res)
def subscription(request):
    res = {}
    res['bodyclass'] = "faimly-friendwraper"
    return render(request,'UserData/user/subscription.html',res)

from operator import itemgetter
def profile(request):
    res = {}
    if request.method == "POST":
        if request.GET.get('profile') == "update":
            profile= request.POST.FILES['my_pics']
            request.user.profile = profile
            request.user.save()
            messages.success(request,"Profile picture updated")
            return redirect(request.path)
        name,gender,dob =  itemgetter('name','gender','dob')(request.POST)
        name = name.strip().split(' ')
        if len(name)>=1:request.user.first_name = name[0]
        if len(name)==2:request.user.last_name = name[1]
        request.user.gender = gender
        request.user.dob = dob
        request.user.save()
        messages.success(request,"Profile updated")
        return redirect(request.path)
    res['bodyclass'] = "faimly-friendwraper"
    return render(request,'UserData/user/profile.html',res)
def booking(request):
    res = {}
    res['bodyclass'] = "faimly-friendwraper"
    return render(request,'UserData/user/booking.html',res)
def report(request):
    res = {}
    res['bodyclass'] = "faimly-friendwraper"
    return render(request,'UserData/user/report.html',res)
def family(request):
    res = {}
    if request.method=="POST":
        form = GenForm(Family)(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Family member added successfully")
            return redirect(request.path)
        else:
            for data in form.errors:
                messages.error(request,str(data))
    res['bodyclass'] = "faimly-friendwraper"
    return render(request,'UserData/user/family.html',res)
from django.core.serializers import serialize


def getMember(request):
    id = request.GET.get('memberid')
    data = serialize('python',Family.objects.filter(id=id))
    return JsonResponse(data[0]['fields'],safe=False)
def address(request):
    res = {}
    res['bodyclass'] = "faimly-friendwraper"
    return render(request,'UserData/user/address.html',res)
