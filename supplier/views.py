from django.shortcuts import render
from rest_framework import generics, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated

from supplier.models import Supplier, SupplierHistory
from supplier.serializers import SupplierSerializer, SupplierHistorySerializer


class SupplierViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''Permissioned viewset of car suppliers.'''
    queryset = Supplier.objects.select_related('user').all()
    serializer_class = SupplierSerializer

    def get_queryset(self):
        current_user = self.request.user
        # print('\n', self.request.user.id, '\n')  # Marker
        if current_user.is_superuser:
            return self.queryset.all()
        else:
            return self.queryset.filter(user=current_user)

    permission_classes = (IsAuthenticated, )


class SupplierHistoryViewSet(viewsets.ModelViewSet):
    '''Viewset of the history of car suppliers.'''
    queryset = SupplierHistory.objects.all()
    serializer_class = SupplierHistorySerializer
