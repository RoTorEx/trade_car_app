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
from django.urls import include, path, re_path
from django.conf import settings
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from admin.swagger import urlpatterns as doc_urls
from user.views import UserProfileViewSet
from buyer.views import BuyerViewSet, BuyerHistoryViewSet, BuyerOfferViewSet
from car.views import CarViewSet
from dealership.views import (DealershipViewSet, DealershipGarageViewSet,
                              DealershipBuyHistoryViewSet, DealershipSaleHistoryViewSet)
from supplier.views import SupplierViewSet, SupplierGarageViewSet


# Application APIs
addresses = (
    (r'user', UserProfileViewSet, 'user'),

    (r'buyer', BuyerViewSet, 'buyer'),
    (r'buyer_history', BuyerHistoryViewSet, 'buyer_history'),
    (r'buyer_offer', BuyerOfferViewSet, 'buyer_offer'),

    (r'car', CarViewSet, 'car'),

    (r'dealership', DealershipViewSet, 'dealership'),
    (r'dealership_garage', DealershipGarageViewSet, 'dealership_garage'),
    (r'dealership_buy', DealershipBuyHistoryViewSet, 'dealership_buy'),
    (r'dealership_sale', DealershipSaleHistoryViewSet, 'dealership_sale'),

    (r'supplier', SupplierViewSet, 'supplier'),
    (r'supplier_garage', SupplierGarageViewSet, 'supplier_garage'),
)

# Route API registrations
router = routers.DefaultRouter()  # List of routers at http://.../api
for addr in addresses:
    router.register(addr[0], addr[1], basename=addr[2])
    # print(router.urls)  # Marker

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('auth/', include('user.urls')),

    path('', include('core.urls')),
]

urlpatterns += doc_urls  # Add Swagger

# Debug toolbar
if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls))
    ] + urlpatterns
