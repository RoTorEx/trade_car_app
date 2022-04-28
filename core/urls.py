from django.urls import path, re_path

from core.views import index


urlpatterns = [
    path('', index, name='home'),
]
