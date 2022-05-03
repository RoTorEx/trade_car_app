from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404
from rest_framework import viewsets


def index(request):  # HttpRequest
    return HttpResponse("Welcome, dude, to main app page!")
