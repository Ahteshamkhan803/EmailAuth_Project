from django.contrib import admin
from EmailAuth_App.models import TempUser


class tempUser_admin(admin.ModelAdmin):
    list_display=['username','password','email','otp','otp_created_at']
admin.site.register(TempUser,tempUser_admin)    
   
