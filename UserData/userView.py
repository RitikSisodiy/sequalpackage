from ast import Not
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http import JsonResponse,HttpResponse
from UserData.models import Family,Booking,report,userAddress
from django.conf import settings
from superuser.forms import GenForm
import mimetypes

def download_file(filepath):
    # Define Django project base directory
    # Define text file name
    filename = 'report'+ filepath[filepath.rfind('.'):]
    # Define the full file path
    print(filepath)
    filepath = settings.MEDIA_ROOT / filepath
    # Open the file for reading content
    print(filepath)

    path = open(filepath, 'rb')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(filepath)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % filename
    # Return the response value
    return response


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
    res['Bookings'] = Booking.objects.filter(user=request.user.id , status='success')
    return render(request,'UserData/user/booking.html',res)
def Report(request,slug=None):
    if slug is not None:
        repofile = report.objects.get(id=slug).report
        return download_file(str(repofile))
    res = {}
    res['reports'] = report.objects.filter(booking__user=request.user)
    res['bodyclass'] = "faimly-friendwraper"
    return render(request,'UserData/user/report.html',res)
def family(request):
    res = {}
    if request.method=="POST":
        form = GenForm(Family)(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Family member added successfully")
        else:
            for data in form.errors:
                messages.error(request,str(data))
        return redirect(request.path)
    res['bodyclass'] = "faimly-friendwraper"
    return render(request,'UserData/user/family.html',res)
from django.core.serializers import serialize


def getMember(request):
    id = request.GET.get('memberid')
    data = serialize('python',Family.objects.filter(id=id))
    return JsonResponse(data[0]['fields'],safe=False)
def address(request):
    if request.method == "POST":
        form = GenForm(userAddress)(request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Thanks for contacting us We will get back to you soon')
        else:
            for key,value in form.errors.as_data().items():
                msg = ""
                for data in value:
                    for v in data:
                        msg+=str(v)+"<br>"
                msg = msg[:msg.rfind('<br>')]
                messages.error(request,f"{key}: {msg}")
            
    res = {}
    res['bodyclass'] = "faimly-friendwraper"
    res['address'] = userAddress.objects.all()
    return render(request,'UserData/user/address.html',res)
