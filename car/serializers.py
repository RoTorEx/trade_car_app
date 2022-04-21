from rest_framework import serializers
from car.models import Car, CarPrice, CarCharacters


class CarSerializer(serializers.ModelSerializer):
    '''Auto serializer.'''
    class Meta:
        model = Car
        fields = '__all__'


class CarPriceSerializer(serializers.ModelSerializer):
    '''Auto price serializer.'''
    class Meta:
        model = CarPrice
        fields = '__all__'


class CarCharactersSerializer(serializers.ModelSerializer):
    '''Serializer of car characteristics.'''
    class Meta:
        model = CarCharacters
        fields = '__all__'
