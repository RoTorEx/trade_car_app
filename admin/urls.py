"""
admin URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from buyer.views import *
from car.views import *
from core.views import *
from dealership.views import *
from supplier.views import *


# API адреса приложений
addresses = (
    (r'buyer', BuyerViewSet),
    (r'buyer_history', BuyerHistoryViewSet),

    (r'car', CarViewSet),
    (r'car_price', CarPriceViewSet),
    (r'car_characters', CarCharactersViewSet),

    (r'offer', OfferViewSet),
    (r'promotion', PromotionViewSet),

    (r'dealership', DealershipViewSet),
    (r'dealership_history', DealershipHistoryViewSet),

    (r'supplier', SupplierViewSet),
    (r'supplier_history', SupplierHistoryViewSet),
)

router = routers.DefaultRouter()
# Регистрации API маршрутов
for addr in addresses:
    router.register(addr[0], addr[1])

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
