from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import StaffLoginView, myaccount

urlpatterns = [
    path("lfk/kundebruker/secure/login/ektelogin/", StaffLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("lfk/kundebruker/secure/login/", myaccount, name="myaccount"),
]
