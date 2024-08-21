from django.shortcuts import redirect, render
# from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .helper import * 
from .models import*
import uuid
# Create your views here.
def home(request):
        return render(request,'acount/index.html')
def signup(request):
    if request.method=='POST':
           username=request.POST['username']
           fname=request.POST['fname']
           lname=request.POST['lname']
           Email=request.POST['email']
           pass1=request.POST['pass1']
           pass2=request.POST['pass2']
           if User.objects.filter(username=username):
                messages.error(request,'user name already exist! please try some other username')
                return redirect('/home/')
           
           if User.objects.filter(email=Email):
                messages.error(request,'Email already rejistered')
                return redirect('/home/')
           


           if len(username)>15:
                messages.error(request,'the user name must be under 15 characters ')
                
           

           if pass1!=pass2:
                messages.error(request,'password does not match')

           if not username.isalnum():
                messages.error(request,'User name must be alpha numeric')
                return redirect('/home/')    



           myuser=User.objects.create_user(username,Email,pass1)
           myuser.first_name=fname
           myuser.last_name=lname

           myuser.save()
           send_email_User(myuser.email)
           messages.success(request,'your acount has been created successfuly.we have setnt you a confirmation email,please confirm your email in order to activate your acount ')
           #welcome email
           

           
           return redirect('/signin/')
    return render(request,'acount/signup.html')
def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        pass1=request.POST['pass1']
        user=authenticate(username=username,password=pass1)
        if user is not None:
             login(request,user)
             fname=user.first_name
             return render(request,'acount/index.html',{'fname':fname})
        else:
             messages.error(request,'Bad credentials')
             return redirect('/home/')
    return render(request,'acount/signin.html')

def signout(request):
    logout(request)
    messages.success(request,'you are successfuly log out ')
    return redirect('/')
def forget_password(request):
     if request.method=='POST':
          username=request.POST.get('username')

          if not User.objects.filter(username=username).exists():
               messages.error(request,'Uer not found with this name')
               return redirect('/froget_password/')
          user_obj=User.objects.get(username=username) 
          token=str(uuid.uuid4())
          profile_obj=profile.objects.get(user=user_obj)
          profile_obj.forget_password_token=token
          profile_obj.save()
          send_forget_password_mail(user_obj.user.email,token)  
          messages.success(request,'an email is sent')
          return redirect('/froget_password/') 
     
     return render (request,'acount/forget_password.html')
def change_password(request,token):
     context={}
     try:
          profile_obj=profile.objects.filter( forget_password_token=token)
          user=profile_obj.user
          if request.method=='POST':
               new_password=request.POST.get('new_password')
               confirm_password=request.POST.get('confirm_password')


               if new_password!=confirm_password:
                    messages.error(request,'Both password should be match')
                    return redirect(f'/change_password/{token}/')
              
               user.set_password(new_password)
               user.save()
               messages.success(request,'password change successfuly , please signin ')
               return redirect('/signin/')
          context={'token':token}
         


     except profile.DoesNotExist:
          messages.error(request,'invalid or expired token')
          return redirect('/forget_password/')
          
     return render(request,'acount/change_password.html',context)