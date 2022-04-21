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

from buyer.views import BuyerViewSet, BuyerHistoryViewSet
from car.views import CarViewSet, CarPriceViewSet, CarCharactersViewSet
from core.views import OfferViewSet, PromotionViewSet
from dealership.views import DealershipViewSet, DealershipHistoryViewSet
from supplier.views import SupplierViewSet, SupplierHistoryViewSet


# Application APIs
addresses = (
    (r'buyer', BuyerViewSet, 'buyer'),
    (r'buyer_history', BuyerHistoryViewSet, 'buyer_history'),

    (r'car', CarViewSet, 'car'),
    (r'car_price', CarPriceViewSet, 'car_price'),
    (r'car_characters', CarCharactersViewSet, 'car_characters'),

    (r'offer', OfferViewSet, 'offer'),
    (r'promotion', PromotionViewSet, 'promotion'),

    (r'dealership', DealershipViewSet, 'dealership'),
    (r'dealership_history', DealershipHistoryViewSet, 'dealership_history'),

    (r'supplier', SupplierViewSet, 'supplier'),
    (r'supplier_history', SupplierHistoryViewSet, 'supplier_history'),
)

# Route API registrations
router = routers.DefaultRouter()  # List of routers at http://.../api
for addr in addresses:
    router.register(addr[0], addr[1], basename=addr[2])
    print(router.urls, end='\n\n\n')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls))
]
