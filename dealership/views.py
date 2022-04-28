from django.shortcuts import render
from rest_framework import generics, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated

from dealership.models import Dealership, DealershipHistory
from dealership.serializers import DealershipSerializer, DealershipHistorySerializer


class DealershipViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    '''Permissioned viewset of car dealerships.'''
    queryset = Dealership.objects.select_related('user').all()
    serializer_class = DealershipSerializer

    def get_queryset(self):
        current_user = self.request.user
        # print('\n', self.request.user.id, '\n')  # Marker
        if current_user.is_superuser:
            return self.queryset.all()
        else:
            return self.queryset.filter(user=current_user)

    permission_classes = (IsAuthenticated, )


class DealershipHistoryViewSet(viewsets.ModelViewSet):
    '''Viewset of the history of car dealerships.'''
    queryset = DealershipHistory.objects.all()
    serializer_class = DealershipHistorySerializer
