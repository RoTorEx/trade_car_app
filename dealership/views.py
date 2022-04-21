from django.shortcuts import render
from rest_framework import viewsets

from dealership.models import Dealership, DealershipHistory
from dealership.serializers import DealershipSerializer, DealershipHistorySerializer


class DealershipViewSet(viewsets.ModelViewSet):
    '''Viewset of car dealerships.'''
    queryset = Dealership.objects.all()
    serializer_class = DealershipSerializer


class DealershipHistoryViewSet(viewsets.ModelViewSet):
    '''Viewset of the history of car dealerships.'''
    queryset = DealershipHistory.objects.all()
    serializer_class = DealershipHistorySerializer
