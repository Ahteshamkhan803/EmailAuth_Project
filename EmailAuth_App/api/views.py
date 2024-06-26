
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from EmailAuth_App.models import TempUser
from EmailAuth_App.api.serializers import Register_serializer,otpVerification_serializer
from .utils import generate_otp, send_otp
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken



class RegisterView(APIView):
    def get(self, request):
        return render(request, 'register.html')
    

    def post(self, request):
        serializer = Register_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = generate_otp()
            temp_user = TempUser.objects.create(
                username=serializer.validated_data['username'],
                email=email,
                password=serializer.validated_data['password'],
                otp=otp
            )
            send_otp(email, otp)
            return redirect('verify_otp', email=email)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
          










class OTPVerificationView(APIView):
    def get(self, request,email=None):
        return render(request, 'otp_verification.html',{'email': email})
    

    def post(self, request,email):
        serializer = otpVerification_serializer(data=request.data)
        if serializer.is_valid():
            # email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            try:
                temp_user = TempUser.objects.get(email=email, otp=otp)
                if timezone.now() > temp_user.otp_created_at + timezone.timedelta(minutes=1):
                    temp_user.delete()
                    return redirect('otpExpire')
                
                user = User.objects.create_user(
                    username=temp_user.username,
                    email=temp_user.email,
                    password=temp_user.password
                )
                temp_user.delete()
                return redirect('login')
            
            except TempUser.DoesNotExist:
                    return redirect('otpExpire')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class LoginView(APIView):
    def get(self, request):
        return render(request, 'login.html')

    def post(self,request):
        username= request.data.get('username')
        password= request.data.get('password')
        user= authenticate(request,username=username, password=password)

        if user is not None:
            login(request,user)
            refresh= RefreshToken.for_user(user)
            request.session['Token'] = str(refresh.access_token)
            return redirect('home')
        return render(request, 'login.html', {'errors' : 'Invalid credentials'})





@login_required   
def home_view(request):
    return render(request, 'home.html', {'username': request.user})


class otpExpired(APIView):
     def get(self,request):
          message= 'Otp is expired'
          return render(request, 'otpExpire.html', {'message':message})     