from django.urls import path
from user.views import RegisterView, LoginAPIView, VerifyEmail

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('email_verify/', VerifyEmail.as_view(), name='email_verify'),
]
