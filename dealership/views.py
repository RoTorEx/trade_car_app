from django.shortcuts import render
from rest_framework import viewsets

from .models import *
from .serializers import *


class DealershipViewSet(viewsets.ModelViewSet):
    '''Вьюсет автосалонов.'''
    queryset = Dealership.objects.all()
    serializer_class = DealershipSerializer


class DealershipHistoryViewSet(viewsets.ModelViewSet):
    '''Вьюсет истории автосалонов.'''
    queryset = DealershipHistory.objects.all()
    serializer_class = DealershipHistorySerializer
