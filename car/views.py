from django.shortcuts import render
from rest_framework import viewsets

from car.models import Car, CarPrice, CarCharacters
from car.serializers import CarSerializer, CarPriceSerializer, CarCharactersSerializer


class CarViewSet(viewsets.ReadOnlyModelViewSet):
    '''Viewset for car models.'''
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class CarPriceViewSet(viewsets.ReadOnlyModelViewSet):
    '''Viewset for car prices.'''
    queryset = CarPrice.objects.all()
    serializer_class = CarPriceSerializer


class CarCharactersViewSet(viewsets.ReadOnlyModelViewSet):
    '''Viewset for machine characteristics.'''
    queryset = CarCharacters.objects.all()
    serializer_class = CarCharactersSerializer
