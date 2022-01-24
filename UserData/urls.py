
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
    path('report/',userView.report,name="report"),
    path('family/',userView.family,name="family"),
    path('getmember/',userView.getMember,name="getmember"),
    path('address/',userView.address,name="address"),
    path('logout/',views.Logout,name="logoutuser"),
]
