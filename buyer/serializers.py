from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from buyer.models import Buyer, BuyerHistory, BuyerOffer
from user.models import UserProfile


class UserBuyerSerializer(serializers.ModelSerializer):
    '''Buyer user serializer.'''
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'role', 'email', 'verifyed_email', 'is_superuser']


class BuyerSerializer(serializers.ModelSerializer):
    '''Buyer serializer.'''
    user = UserBuyerSerializer(read_only=True)

    class Meta:
        model = Buyer
        fields = ['id', 'user', 'first_name', 'last_name', 'balance_currency', 'balance', 'is_active']


class BuyerOfferSerializer(serializers.ModelSerializer):
    '''Buyer offer serializer.'''
    preferred_car_characters = serializers.JSONField(required=False, initial=dict)

    class Meta:
        model = BuyerOffer
        fields = '__all__'


class BuyerHistorySerializer(serializers.ModelSerializer):
    '''Buyer history serializer.'''
    class Meta:
        model = BuyerHistory
        fields = '__all__'
