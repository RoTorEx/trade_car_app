from rest_framework import serializers

from dealership.models import Dealership, DealershipGarage, DealershipBuyHistory, DealershipSaleHistory
from user.models import UserProfile


class UserDealershipSerializer(serializers.ModelSerializer):
    '''Dealership user serializer.'''
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'role', 'email', 'verifyed_email', 'is_superuser']


class DealershipSerializer(serializers.ModelSerializer):
    '''Dealership serializer.'''
    user = UserDealershipSerializer(read_only=True)

    class Meta:
        model = Dealership
        fields = ['id', 'user', 'name', 'location', 'balance', 'is_active']


class DealershipGarageSerializer(serializers.ModelSerializer):
    '''Dealership cars serializer.'''
    class Meta:
        model = DealershipGarage
        fields = '__all__'


class DealershipBuyHistorySerializer(serializers.ModelSerializer):
    '''Dealership cars serializer.'''
    class Meta:
        model = DealershipBuyHistory
        fields = '__all__'


class DealershipSaleHistorySerializer(serializers.ModelSerializer):
    '''Dealership cars serializer.'''
    class Meta:
        model = DealershipSaleHistory
        fields = '__all__'
