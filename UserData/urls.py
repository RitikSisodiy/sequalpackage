
from django.urls import path 
from . import views , userView
urlpatterns = [
    path('login', views.LoginSignUp , name="userlogin"),
    path('login/verifyotp', views.verifyotp , name="verifyotp"),
    path('registration/',views.registration,name="registration"),
    path('dashboard/',userView.dashboard,name="userdashboard"),
    # path('subscription/',userView.subscription,name="subscription"),
    path('profile/',userView.profile,name="profile"),
    path('booking/',userView.booking,name="booking"),
    path('report/',userView.Report,name="report"),
    path('report/report<slug:slug>/download',userView.Report,name="reportdownload"),
    path('family/',userView.family,name="family"),
    path('getmember/',userView.getMember,name="getmember"),
    path('deletemember/<int:id>',userView.deleteMember,name="deletemember"),
    path('address/',userView.address,name="address"),
    path('getaddress/',userView.getaddress,name="getaddress"),
    path('deleteaddress/<int:id>/',userView.deleteaddress,name="deleteaddress"),
    path('logout/',views.Logout,name="logoutuser"),
]
