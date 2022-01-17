from django.shortcuts import redirect, render

def dashboard(request):
    res={}
    res['bodyclass'] = "dashboard"
    return render(request,'UserData/user/dashboard.html',res)
def subscription(request):
    res = {}
    res['bodyclass'] = "faimly-friendwraper"
    return render(request,'UserData/user/subscription.html',res)
def profile(request):
    res = {}
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
    res['bodyclass'] = "faimly-friendwraper"
    return render(request,'UserData/user/family.html',res)
def address(request):
    res = {}
    res['bodyclass'] = "faimly-friendwraper"
    return render(request,'UserData/user/address.html',res)
