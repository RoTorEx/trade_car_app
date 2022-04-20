from django.shortcuts import render
from rest_framework import viewsets

from .models import *
from .serializers import *


class CarViewSet(viewsets.ReadOnlyModelViewSet):
    '''Вьюсет для моделей машин.'''
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarPriceViewSet(viewsets.ReadOnlyModelViewSet):
    '''Вьюсет для моделей машин.'''
    queryset = CarPrice.objects.all()
    serializer_class = CarPriceSerializer


class CarCharactersViewSet(viewsets.ReadOnlyModelViewSet):
    '''Вьюсет для характеристик машин.'''
    queryset = CarCharacters.objects.all()
    serializer_class = CarCharactersSerializer
