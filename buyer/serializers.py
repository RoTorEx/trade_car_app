from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from buyer.models import Buyer, BuyerHistory


class BuyerSerializer(serializers.ModelSerializer):
    '''Buyer serializer.'''
    class Meta:
        model = Buyer
        fields = '__all__'


class BuyerHistorySerializer(serializers.ModelSerializer):
    '''Buyer history serializer.'''
    class Meta:
        model = BuyerHistory
        fields = '__all__'


# class BuyerModel:
#     '''Определили класс, объекты которого будем сериализовать.'''
#     def __init__(self, first_name, last_name):
#         self.first_name = first_name
#         self.last_name = last_name


# class BuyerSerializer(serializers.Serializer):
#     '''Класс сериализации данных.'''
#     first_name = serializers.CharField(max_length=255)
#     last_name = serializers.CharField(max_length=255)


# def encode():
#     model = BuyerModel("Aleksey Strelkov", "Valeriy Visotsky")
#     model_sr = BuyerSerializer(model)
#     print(model_sr.data, type(model_sr.data), sep='\n')
#     json = JSONRenderer().render(model_sr.data)  # Преобразует объект сериализации в байтовую json строку
#     print(json)
