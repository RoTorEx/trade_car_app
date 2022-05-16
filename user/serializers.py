from rest_framework import serializers

from user.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    '''Users profile serializer.'''

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'role', 'email', 'verifyed_email', 'is_superuser']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # max_length=68, min_length=6,

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
