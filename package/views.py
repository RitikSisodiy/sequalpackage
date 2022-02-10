from unittest import result
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from razorpay import Order, Payment
from .models import package, tempbooking,Subcategory,test,category,coupon
from UserData.models import cart,Family,Booking, userAddress
from datetime import datetime
from itertools import chain
from paymentintigration.views import getPaytmParam, verifyPaymentRequest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
def packagedetails(request,slug):
    res = {}
    res['package'] = package.objects.get(slug=slug)
    qry = [data['id'] for data in res['package'].package_category.all().values('id')]
    res['related'] = package.objects.filter(package_category__in=qry).exclude(slug=slug).distinct()
    print(res['related'])
    # print(res['package'].package_category.all().values_list('id'))
    totaltest = 0
    for data in res['package'].Porfile_collection.all():
        totaltest += data.Select_Test_id.all().count()
    res['totaltest'] = totaltest
    return render(request,'package/packageDetails.html',res)
def testdetails(request,slug):
    res = {}
    res['package'] = test.objects.get(slug=slug)
    qry = [data['id'] for data in res['package'].test_category.all().values('id')]
    res['related'] = test.objects.filter(test_category__in=qry).exclude(slug=slug).distinct()
    totaltest = 0
    res['totaltest'] = totaltest
    return render(request,'package/testDetails.html',res)

def getbycategory(request,slug='slug'):
    res= {}
    res['bodyclass'] = "risk-page"
    return render(request,'package/listpackage.html',res) 
def getbysubcategory(request,subcategory=None,catename=None,type='package'):
    res= {}
    if subcategory is not None:
        slug = subcategory
        res['category'] = Subcategory.objects.get(slug=slug)
    if catename is not None:
        slug = catename
        res['category'] = category.objects.get(slug=slug)
    res['type'] = type
    res['bodyclass'] = "risk-page"
    res['subcate'] = subcategory
    page = request.GET.get('page', 1)
    if type=='test':
        # print('working')
        if subcategory is not None:
            res['packages'] = test.objects.filter(test_category__slug=slug,Publish='1')
        else:
            res['packages'] = test.objects.filter(test_category__category__slug=slug,Publish='1')
    else:
        if subcategory is not None:
            res['packages'] = package.objects.filter(package_category__slug=slug,Publish='1')
        else:
            res['packages'] = package.objects.filter(package_category__category__slug=slug,Publish='1')
    res['packages'] = res['packages'].distinct()
    res['packages'] =Paginator(res['packages'], 12)
    try:
        res['packages'] = res['packages'].page(page)
    except PageNotAnInteger:
        res['packages'] = res['packages'].page(1)
    except EmptyPage:
        res['packages'] = res['packages'].page(res['packages'].num_pages)
    return render(request,'package/listpackage.html',res) 
    

@login_required(login_url='userlogin')
def booknow(request,slug,type):
    res= {}
    res['member'] = request.user.Family.all()
    if type=='package':
        buypackage = package.objects.get(slug=slug)
        totaltest = 0
        for data in buypackage.Porfile_collection.all():
            totaltest += data.Select_Test_id.all().count()
        res['totaltest'] = totaltest
        res['totleprize'] = float(buypackage.final_cost)*(res['member'].count()+1)
        res['totalsaving'] =(float(buypackage.Package_price) -float(buypackage.final_cost))*res['member'].count()
        buytest = None
    else:
        buypackage = None
        buytest = test.objects.get(slug=slug)
        res['totleprize'] = float(buytest.final_cost)*(res['member'].count()+1)
        res['totalsaving'] =(float(buytest.test_price) -float(buytest.final_cost))*res['member'].count()
    res['type'] = type
    res['package'] = buypackage
    res['test'] =buytest
    res['address'] = userAddress.objects.filter(user=request.user.id)
    cart.objects.update_or_create(user=request.user,package=buypackage,test=buytest)
    res['family'] = Family.objects.filter(user= request.user)
    if request.method=="POST":
        print(request.POST)
        date = request.POST['colletiondate']
        time = request.POST['colletiontime']
        datime = datetime.strptime(date+" "+time,'%Y-%m-%d %H:%M')
        address = request.POST['address']
        coupencode = request.POST['coupencode']
        address = res['address'].filter(id=address)[0]
        paymode = request.POST['payoption']
        forself = True if request.POST['self'] == 'on' else False
        familymember = []
        for data in request.POST:
            val = request.POST[data]
            if 'member' in data and val == "on":
                familymember.append(data)
        bookingids = ''
        ammount = 0.0
        tran = tempbooking(user=request.user,ammount=0)
        tran.save()
        for data in familymember:
            mem = Family.objects.get(id=data.replace('member',''))
            newbooking = Booking(user=request.user,type=type,package=buypackage,test=buytest,collectiontime=datime,bookingfor=data,member=mem,address=address)
            newbooking.save()
            if buypackage is not None:
                ammount+=float(buypackage.final_cost)
            else:
                ammount+=float(buytest.final_cost)
            tran.bookingid.add(newbooking)
        if forself:
            newbooking = Booking(user=request.user,type=type,package=buypackage,test=buytest,collectiontime=datime,bookingfor='self',address=address)
            newbooking.save()
            if buypackage is not None:
                ammount+=float(buypackage.final_cost)
            else:
                ammount+=float(buytest.final_cost)
            tran.bookingid.add(newbooking)
        tran.ammount = ammount
        tran.save()
        validate = validateCoupen(request,coupencode,ammount)
        print(validate)
        if validate['success']:
            tran.coupon = validate['code']
            discount = validate['discount']
            amm = tran.ammount
            if '%' in discount:
                dis = float(discount.replace('%',''))
                tran.ammount = amm -((amm*dis)/100)
            else:
                tran.ammount = amm - float(discount)
        tran.save()
        print(tran.ammount)
        if paymode == "paytm":
            return getPaytmParam(request,tran.tempbookingid,tran.ammount,request.user.phone,'handlePaytm',"INR")
        elif paymode == "cod":
            tempbook = tempbooking.objects.get(tempbookingid = tran.tempbookingid)
            tempbook.status = 'success'
            tempbook.save()
            for data in tempbook.bookingid.split(','):
                if len(data)>0:
                    bob =Booking.objects.get(id=data)
                    bob.status="cod"
                    bob.save()
            return render(request,'package/paymentstatus.html',{'response': {'RESPCODE':'01'}})
        return redirect(request.path)
    return render(request,'package/booknow.html',res)
@csrf_exempt
def handlepaytm(request):
    print(request.POST)
    verify,response_dict = verifyPaymentRequest(request)
    if verify:
        if response_dict['RESPCODE'] == '01':
            tempbook = tempbooking.objects.get(tempbookingid = response_dict['ORDERID'])
            tempbook.status = 'success'
            tempbook.save()
            for bob in tempbook.bookingid.all():
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

def Test(request):
    numbers_list = range(1, 1000)
    page = request.GET.get('page', 1)
    paginator = Paginator(numbers_list, 20)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)
    return render(request, 'package/test1.html', {'numbers': numbers})
def searchinModel(modelname,qry):
    if qry is not None:
        print('if working')
        from django.db.models import  Q
        from django.db.models import CharField
        fields = [f for f in modelname._meta.fields if isinstance(f, CharField)]
        queries = [Q(**{f.name+'__contains': qry}) for f in fields]
        qs = Q()
        for query in queries:
            qs = qs | query
        print(qs)
        res = modelname.objects.filter(qs)
        return res
    return []
def search(request):
    res={}
    res['bodyclass'] = "risk-page"
    qry = request.GET.get('q')
    page = request.GET.get('page',None)
    if qry is not None:
        # searchresult = chain(searchinModel(package,qry),searchinModel(test,qry))
        # searchresult = []
        # for data in searchinModel(test,qry):
        #     searchresult.append(data)
        # for data in searchinModel(package,qry):
        #     searchresult.append(data)
        searchresult = list(chain(searchinModel(test,qry),searchinModel(package,qry)))
        # if searchresult:
        #     searchresult = [searchresult[0] for data in range(0,100)]
        paginator = Paginator(searchresult, 12)
        try:
            result = paginator.page(page)
        except PageNotAnInteger:
            result = paginator.page(1)
        except EmptyPage:   
            result = paginator.page(paginator.num_pages)
        res['result'] = result
    return render(request,'package/search.html',res)

def validateCoupen(request,code,ordervalue):
    res= {}
    res['code'] = code
    res['success'] = False
    if code is None or len(code)==0:
        res['message'] = "please add coupen code"
        res
    couponob = coupon.objects.filter(Generate_coupon=code,active='1')
    if not couponob.exists():
        res['message'] = "Please Enter a valid coupen code"
        return res
    couponob = couponob[0]
    if  datetime.now().date() > couponob.Coupon_expire_date:
        res['message'] = "This Coupen is expired"
        return res
    if tempbooking.objects.filter(user=request.user.id,coupon=code,status='success').exists():
        res['message'] = "You Already Used This Coupen"
        return res
    if couponob.minimum_order_value > float(ordervalue):
        res['message'] = f'minimum ₹{couponob.minimum_order_value} ordervalue is required'
        return res
    res['success'] = True
    res['message']=couponob.message
    res['discount'] = couponob.discount
    return res
@login_required(login_url='userlogin')
def getCoupenDetails(request):
    code = request.GET.get('coupen')
    ordervalue = request.GET.get('ordervalue')
    res= validateCoupen(request,code,ordervalue)
    return JsonResponse(res)
    