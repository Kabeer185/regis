from django.contrib import admin
from django.urls import path
from  .import views

urlpatterns = [
    path('',views.home,name='home'),
    path ('signup/',views.signup,name='signup'),
    path ('signin/',views.signin,name='signin'),
    path ('forget_password/',views.forget_password,name='forget_password'),
    path ('change_password/<str:token>/',views.change_password,name='change_password'),
    path ('signout/',views.signout,name='signout'),

]
