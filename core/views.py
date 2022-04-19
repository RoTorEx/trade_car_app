from django.shortcuts import render
from rest_framework import viewsets

from .models import *
from .serializers import *


class OfferViewSet(viewsets.ModelViewSet):
    '''Вьюсет заказов на авто.'''
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class PromotionViewSet(viewsets.ModelViewSet):
    '''Вьюсет акций.'''
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
