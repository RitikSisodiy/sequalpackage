import re
from django.forms import models
from django.http import request
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from UserData.userView import booking

from .models import package, tempbooking
from UserData.models import cart,Family,Booking
from datetime import datetime
from paymentintigration.views import getPaytmParam, verifyPaymentRequest
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
    res= {}
    buypackage = package.objects.get(slug=slug)
    cart.objects.update_or_create(user=request.user,package=buypackage)
    res['family'] = Family.objects.filter(user= request.user)
    if request.method=="POST":
        print(request.POST)
        date = request.POST['colletiondate']
        time = request.POST['colletiontime']
        datime = datetime.strptime(date+" "+time,'%Y-%m-%d %H:%M')
        forself = True if request.POST['self'] == 'on' else False
        familymember = []
        for data in request.POST:
            val = request.POST[data]
            if 'member' in data and val == "on":
                familymember.append(data)
        bookingids = ''
        ammount = 0.0
        for data in familymember:
            mem = Family.objects.get(id=data.replace('member',''))
            newbooking = Booking(user=request.user,type='package',package=buypackage,collectiontime=datime,bookingfor=data,member=mem)
            newbooking.save()
            ammount+=float(buypackage.final_cost)
            bookingids+=str(newbooking.id)+","
        if forself:
            newbooking = Booking(user=request.user,type='package',package=buypackage,collectiontime=datime,bookingfor='self')
            newbooking.save()
            ammount+=float(buypackage.final_cost)
            bookingids += str(newbooking.id)
        tran = tempbooking(bookingid=bookingids,ammount=ammount)
        tran.save()
        return getPaytmParam(request,tran.tempbookingid,tran.ammount,request.user.phone,'handlePaytm',"INR")
        return html
    return render(request,'package/booknow.html',res)
@csrf_exempt
def handlepaytm(request):
    print(request.POST)
    verify,response_dict = verifyPaymentRequest(request)
    if verify:
        if response_dict['RESPCODE'] == '01':
            tempbook = tempbooking.objects.get(tempbookingid = response_dict['ORDERID'])
            for data in tempbook.bookingid.split(','):
                if len(data)>0:
                    bob =Booking.objects.get(id=data)
                    bob.status="success"
                    bob.save()
            response_dict['couse'] = float(response_dict['TXNAMOUNT'])
        else:
            try:
                tempbook = tempbooking.objects.get(tempbookingid = response_dict['ORDERID'])
                for data in tempbook.bookingid.split(','):
                    if len(data)>0:
                        bob =Booking.objects.get(id=data)
                        bob.delete()
            except Exception as e:
                pass
    else:
            print("order unsuccessful because",response_dict['RESPMSG'])
    return render(request,'package/paymentstatus.html',{'response': response_dict})