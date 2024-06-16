
from django.urls import path
from .views import RegisterView, OTPVerificationView,LoginView,home_view,otpExpired






urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify_otp/<str:email>/', OTPVerificationView.as_view(), name='verify_otp'),
    path('login/', LoginView.as_view(), name='login'),
    path('home/',home_view.as_view(), name='home' ),
    path('Otp-is-Expired/',otpExpired.as_view(),name='otpExpire')
]
