from django.shortcuts import render
from rest_framework import generics, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from dealership.models import Dealership, DealershipGarage, DealershipBuyHistory, DealershipSaleHistory
from dealership.serializers import (DealershipSerializer, DealershipGarageSerializer,
                                    DealershipBuyHistorySerializer, DealershipSaleHistorySerializer)
from core.service import DealershipFilter


class DealershipViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    '''Permissioned viewset of car dealerships.'''
    queryset = Dealership.objects.select_related('user').all()
    serializer_class = DealershipSerializer

    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    search_fields = ('name', )
    ordering_fields = ('name', 'location', 'balance')
    filterset_class = DealershipFilter

    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_superuser:
            return self.queryset.all()
        else:
            return self.queryset.filter(user=current_user)

    permission_classes = (IsAuthenticated, )


class DealershipGarageViewSet(viewsets.ReadOnlyModelViewSet):
    '''Viewset of dealership's cars.'''
    queryset = DealershipGarage.objects.all()
    serializer_class = DealershipGarageSerializer


class DealershipBuyHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    '''History viewset of bought cars.'''
    queryset = DealershipBuyHistory.objects.all()
    serializer_class = DealershipBuyHistorySerializer


class DealershipSaleHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    '''History viewset of sold cars.'''
    queryset = DealershipSaleHistory.objects.all()
    serializer_class = DealershipSaleHistorySerializer
