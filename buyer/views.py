from django.shortcuts import render
from django.forms import model_to_dict
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from buyer.models import Buyer, BuyerHistory
from buyer.serializers import BuyerSerializer, BuyerHistorySerializer


class BuyerViewSet(viewsets.ModelViewSet):
    '''Viewset of buyers. ModelViewSet means all API requests are available.'''
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer


class BuyerHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    '''Viewset of customer history. ReadOnlyModelViewSet only allows data to be read.'''
    queryset = BuyerHistory.objects.all()
    serializer_class = BuyerHistorySerializer


# class BuyerAPIView(generics.ListAPIView):
#     '''Класс представления API.'''
#     queryset = Buyer.objects.all()
#     serializer_class = BuyerSerializer


# class BuyerAPIView(APIView):
#     '''
#     APIView – базовый класс представления, от которого наследуются остальные классы.
#     То есть этот класс работает на самом низком уровне без сериализатора с одним классом представления.
#     '''
#     def get(self, requst):  # Обработка GET запросов на сервер
#         lst = Buyer.objects.all().values()
#         return Response({'Buyers': list(lst)})

#     def post(self, request):  # Обработка POST запросов. Добавляет запись и возвращает то, что добавили
#         post_new = Buyer.objects.create(
#             first_name=request.data['first_name'],
#             last_name=request.data['last_name'],
#             email_address=request.data['email_address'],
#             balance=request.data['balance'])
#         return Response({'post': model_to_dict(post_new)})  # Преобразует модель Django в словарь
