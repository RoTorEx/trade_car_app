from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.urls import reverse

from user.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    '''Users profile serializer.'''

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'role', 'email', 'verifyed_email', 'is_superuser']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = UserProfile

        fields = ['username', 'email', 'role', 'password']

    def validate(self, attrs):
        username = attrs.get('username', '')
        email = attrs.get('email', '')

        if not username.isalnum():
            raise serializers.ValidationError("The username must only contain alphanumeric symbols.")

        return attrs

    def create(self, validated_data):
        return UserProfile.objects.create_user(**validated_data)


class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = UserProfile
        fields = ['token']


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=68, min_length=1)
    email = serializers.EmailField(max_length=255, min_length=6, read_only=True)
    password = serializers.CharField(max_length=68, min_length=1, write_only=True)
    tokens = serializers.CharField(max_length=68, min_length=6, read_only=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'tokens']

    def validate(self, attrs):
        username = attrs.get('username', '')
        password = attrs.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials, try again.")

        if not user.is_active:
            raise AuthenticationFailed("Account is disable.")

        return {'username': user.username, 'email': user.email, 'tokens': user.tokens()}


class RequestPasswordResetSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=1)

    class Meta:
        fields = ['username']
