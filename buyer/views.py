from django.shortcuts import render
from django.forms import model_to_dict
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import *
from .serializers import *


class BuyerViewSet(viewsets.ModelViewSet):
    '''Вью сет покупателя. ModelViewSet подразумевает доступными все API запросы.'''
    queryset = Buyer.objects.all()
    serializer_class = BuyerSerializer


class BuyerHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    '''Вью сет истории покуптелей. ReadOnlyModelViewSet разрешает только чтение данных.'''
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
