from rest_framework import serializers

from dealership.models import Dealership, DealershipHistory
from user.models import UserProfile


class UserBuyerSerializer(serializers.ModelSerializer):
    '''Dealership user serializer.'''
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'role', 'email', 'verifyed_email', 'is_superuser']


class DealershipSerializer(serializers.ModelSerializer):
    '''Dealership serializer.'''
    user = UserBuyerSerializer(read_only=True)

    class Meta:
        model = Dealership
        fields = ['id', 'user', 'name', 'location', 'balance_currency', 'balance',
                  'cars', 'cars_price', 'cars_chars', 'buyers', 'is_active']


class DealershipHistorySerializer(serializers.ModelSerializer):
    '''Car showroom history serializer.'''
    class Meta:
        model = DealershipHistory
        fields = '__all__'
