from django.shortcuts import render
from rest_framework import viewsets

from car.models import Car
from car.serializers import CarSerializer


class CarViewSet(viewsets.ModelViewSet):
    '''Viewset for car models.'''
    queryset = Car.objects.all()
    serializer_class = CarSerializer
