from django.contrib import admin
from acount.models import profile

# Register your models here.
@admin.register(profile)
class profileadmin(admin.ModelAdmin):
   list_display = ['user','forget_password_token','created_at']