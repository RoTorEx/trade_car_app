from rest_framework import serializers
from .models import *


class CarSerializer(serializers.ModelSerializer):
    '''Сериализатор авто.'''
    class Meta:
        model = Car
        fields = '__all__'


class CarPriceSerializer(serializers.ModelSerializer):
    '''Сериализатор цен авто.'''
    class Meta:
        model = CarPrice
        fields = '__all__'


class СarCharactersSerializer(serializers.ModelSerializer):
    '''Сериализатор характеристик авто.'''
    class Meta:
        model = СarCharacters
        fields = '__all__'
