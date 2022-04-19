from django.shortcuts import render
from rest_framework import viewsets

from .models import *
from .serializers import *


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer


class SupplierHistoryViewSet(viewsets.ModelViewSet):
    queryset = SupplierHistory.objects.all()
    serializer_class = SupplierHistorySerializer
