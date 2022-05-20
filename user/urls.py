from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from user.views import (RegisterView,
                        LoginAPIView,
                        VerifyEmail,
                        PasswordTokenCkeckAPI,
                        RequestPasswordReset,
                        SetNewPasswordAPIView,
                        ChangeUsername,
                        ChangeEmail)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('email_verify/', VerifyEmail.as_view(), name='email_verify'),
    path('change/username', ChangeUsername.as_view(), name='username_change'),
    path('change/email', ChangeEmail.as_view(), name='email_change'),
    path('request_rest/', RequestPasswordReset.as_view(), name='request_rest'),
    path('password_rest/<uidb64>/<token>', PasswordTokenCkeckAPI.as_view(), name='password_reset_confirm'),
    path('password_reset_complete', SetNewPasswordAPIView.as_view(), name='password_reset_complete'),
]
