from django.shortcuts import render
from rest_framework import generics, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from supplier.models import Supplier, SupplierGarage
from supplier.serializers import SupplierSerializer, SupplierGarageSerializer
from core.service import SupplierFilter


class SupplierViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''Permissioned viewset of car suppliers.'''
    queryset = Supplier.objects.select_related('user').all()
    serializer_class = SupplierSerializer

    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    search_fields = ('name', )
    ordering_fields = ('name', 'year_of_foundation')
    filterset_class = SupplierFilter

    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_superuser:
            return self.queryset.all()
        else:
            return self.queryset.filter(user=current_user)

    permission_classes = (IsAuthenticated, )


class SupplierGarageViewSet(viewsets.ModelViewSet):
    '''Viewset of the history of car suppliers.'''
    queryset = SupplierGarage.objects.all()
    serializer_class = SupplierGarageSerializer
