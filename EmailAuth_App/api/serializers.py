from rest_framework import serializers
from django.contrib.auth.models import User
from EmailAuth_App.models import TempUser






class Register_serializer(serializers.ModelSerializer):
    confirm_password= serializers.CharField(write_only=True)


    class Meta:
        model= TempUser
        fields= ['username', 'email','password','confirm_password']



    def validate(self,data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError('pawweord is not matched')
        return data

class otpVerification_serializer(serializers.Serializer):
    email= serializers.EmailField()
    otp= serializers.CharField(max_length= 6) 



        

