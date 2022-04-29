from django.shortcuts import render
from rest_framework import viewsets
from django.http import HttpResponse, HttpResponseNotFound, Http404

from core.models import Offer, Promotion
from core.serializers import OfferSerializer, PromotionSerializer


class OfferViewSet(viewsets.ModelViewSet):
    '''Viewset of car orders.'''
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer


class PromotionViewSet(viewsets.ModelViewSet):
    '''Promotion viewset.'''
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer


def index(request):  # HttpRequest
    return HttpResponse("Welcome, dude, to main app page!")
