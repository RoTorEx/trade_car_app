from django.shortcuts import render
from rest_framework import generics, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from buyer.models import Buyer, BuyerHistory
from buyer.serializers import BuyerSerializer, BuyerHistorySerializer


class BuyerViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    '''Permissioned viewset of buyers. ModelViewSet means all API requests are available.'''
    queryset = Buyer.objects.select_related('user').all()
    serializer_class = BuyerSerializer

    filter_backends = (DjangoFilterBackend, )
    filter_fields = ['first_name']

    def get_queryset(self):
        current_user = self.request.user
        # print('\n', self.request.user.id, '\n')  # Marker
        if current_user.is_superuser:
            return self.queryset.all()
        else:
            return self.queryset.filter(user=current_user)

    permission_classes = (IsAuthenticated, )


class BuyerHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    '''Viewset of customer history. ReadOnlyModelViewSet only allows data to be read.'''
    queryset = BuyerHistory.objects.all()
    serializer_class = BuyerHistorySerializer
