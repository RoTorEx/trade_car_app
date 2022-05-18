from django.shortcuts import render
from rest_framework import generics, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from buyer.models import Buyer, BuyerHistory, BuyerOffer
from buyer.serializers import BuyerSerializer, BuyerHistorySerializer, BuyerOfferSerializer
from core.service import BuyerFilter, BuyerOfferFilter


class BuyerViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    '''Permissioned viewset of buyers. ModelViewSet means all API requests are available.'''
    queryset = Buyer.objects.select_related('user').all()
    serializer_class = BuyerSerializer

    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    search_fields = ('first_name', )
    ordering_fields = ('user', 'first_name', 'last_name', 'balance')
    filterset_class = BuyerFilter

    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_superuser:
            return self.queryset.all()
        else:
            return self.queryset.filter(user=current_user)

    permission_classes = (IsAuthenticated, )


class BuyerOfferViewSet(viewsets.ModelViewSet):
    '''Viewset of buyer car offer. ReadOnlyModelViewSet only allows data to be read.'''
    queryset = BuyerOffer.objects.all()
    serializer_class = BuyerOfferSerializer

    filter_backends = (filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend)
    ordering_fields = ('active_status', )
    filterset_class = BuyerOfferFilter


class BuyerHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    '''Viewset of buyer history.'''
    queryset = BuyerHistory.objects.all()
    serializer_class = BuyerHistorySerializer
