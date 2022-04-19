from rest_framework import serializers

from .models import *


class OfferSerializer(serializers.ModelSerializer):
    '''Сериализатор заказов.'''
    class Meta:
        model = Offer
        fields = '__all__'


class PromotionSerializer(serializers.ModelSerializer):
    '''Сериализатор акций.'''
    class Meta:
        model = Promotion
        fields = '__all__'
