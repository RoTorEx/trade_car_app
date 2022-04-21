from django.shortcuts import render
from rest_framework import viewsets

from supplier.models import Supplier, SupplierHistory
from supplier.serializers import SupplierSerializer, SupplierHistorySerializer


class SupplierViewSet(viewsets.ModelViewSet):
    '''Viewset of car suppliers.'''
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class SupplierHistoryViewSet(viewsets.ModelViewSet):
    '''Viewset of the history of car suppliers.'''
    queryset = SupplierHistory.objects.all()
    serializer_class = SupplierHistorySerializer
