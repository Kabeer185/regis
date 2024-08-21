from django.core.mail import send_mail
from django.conf import settings
#for signup sned an email
def send_email_User(email):
    subject='cofirm your email'
    message='welcome to the django login page!! please confirm your email to activate your acount'
    from_email=settings.EMAIL_HOST_USER
    to_list=[email]
    send_mail(subject,message,from_email,to_list,fail_silently=True)

# for forget password code
def send_forget_password_mail(email,token):
    subject='your forget password link'
    message=f'Hi, click on the link to reset your password  http://127.0.0.1:8000/change_password/{token}/'
    from_email=settings.EMAIL_HOST_USER
    to_list=[email]
    send_mail(subject,message,from_email,to_list)
    