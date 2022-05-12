from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404
from rest_framework import viewsets

from admin.tasks import hello


def index(request):  # HttpRequest
    hello()
    return HttpResponse("Welcome, dude, to main app page!")
