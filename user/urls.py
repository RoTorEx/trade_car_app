from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import RegisterView, LoginAPIView, VerifyEmail

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('email_verify/', VerifyEmail.as_view(), name='email_verify'),
]
