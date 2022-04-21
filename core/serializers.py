from rest_framework import serializers

from core.models import Offer, Promotion


class OfferSerializer(serializers.ModelSerializer):
    '''Orders serializer.'''
    class Meta:
        model = Offer
        fields = '__all__'


class PromotionSerializer(serializers.ModelSerializer):
    '''Promotion serializer.'''
    class Meta:
        model = Promotion
        fields = '__all__'
