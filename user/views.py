from rest_framework import generics, viewsets, mixins, views
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.encoding import force_str, smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from core.service import UserProfileFilter
from user.models import UserProfile
from user.serializers import (UserProfileSerializer,
                              RegisterSerializer,
                              EmailVerificationSerializer,
                              LoginSerializer,
                              RequestPasswordResetSerializer,
                              SetNewPasswordSerializer,
                              ChangeUsernameSerializer,
                              ChangeEmailSerializer)
from user.utils import send_mail_to_user, verify_user_email


class UserProfileViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    search_fields = ('username',)
    ordering_fields = ('username', 'role', 'email', 'verifyed_email', 'is_superuser')
    filterset_class = UserProfileFilter

    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    @action(detail=False, methods=['get'])
    def me(self, request):
        self.kwargs['pk'] = request.user.pk

        if request.method == 'GET':
            return self.retrieve(request)
        else:
            raise Exception('Not implemented')


class RegisterView(generics.GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = UserProfile.objects.get(username=user_data['username'])
        token = RefreshToken.for_user(user).access_token

        current_site = get_current_site(request).domain
        relativeLink = reverse('email_verify')

        absurl = f"http://{current_site}{relativeLink}?token={str(token)}"
        email_body = f"Hi, {user.username}! Use link below to verify your email:\n{absurl}"

        data = {'email_subject': 'Verify your email', 'email_body': email_body, 'to_email': user.email}

        send_mail_to_user(data)  # Send an email to new user

        return Response(user_data, status=status.HTTP_201_CREATED)


class VerifyEmail(views.APIView):

    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')

        return verify_user_email(token)  # Try to verify user email


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordReset(generics.GenericAPIView):
    serializer_class = RequestPasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        username = request.data['username']

        if UserProfile.objects.filter(username=username).exists():
            user = UserProfile.objects.get(username=username)

            if user.verifyed_email:
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)

                current_site = get_current_site(request=request).domain
                relativeLink = reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})

                absurl = f"http://{current_site}{relativeLink}"
                email_body = f"Hello!\nUse link below to reset you password:\n{absurl}\n\n\n"
                email_body += "If you didn't request a reset then ignore this message."

                data = {'email_subject': 'Reset you password', 'email_body': email_body, 'to_email': user.email}

                send_mail_to_user(data)  # Send an email to new user

                return Response({'success': "We have sent you a link to reset password."}, status=status.HTTP_200_OK)

            return Response({'error': 'Your email is not verify!'}, status=status.HTTP_403_FORBIDDEN)

        return Response({'error': 'Invalid username.'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordTokenCkeckAPI(generics.GenericAPIView):
    def get(self, request, uidb64, token):

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = UserProfile.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token is not valid, please request a new one.'},
                                status=status.HTTP_401_UNAUTHORIZED)

            return Response({
                'success': True,
                'message': 'Credentials Valid',
                'uidb64': uidb64,
                'token': token
            }, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError:
            return Response({'error': 'Token is not valid, please request a new one.'},
                            status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({'success': True, 'message': 'Password reset success.'}, status=status.HTTP_200_OK)


class ChangeUsername(generics.GenericAPIView):
    serializer_class = ChangeUsernameSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({'success': True, 'message': 'Username change success.'}, status=status.HTTP_200_OK)


class ChangeEmail(generics.GenericAPIView):
    serializer_class = ChangeEmailSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response({'success': True, 'message': 'Email change success.'}, status=status.HTTP_200_OK)
