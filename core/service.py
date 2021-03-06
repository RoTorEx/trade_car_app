import django_filters
from django_filters import rest_framework as filters
from django_filters.widgets import BooleanWidget

from user.models import UserProfile
from buyer.models import Buyer, BuyerOffer
from dealership.models import Dealership
from supplier.models import Supplier


class CharFieldInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class UserProfileFilter(filters.FilterSet):
    username = CharFieldInFilter(lookup_expr='iexact')
    email = CharFieldInFilter(lookup_expr='iexact')
    verifyed_email = django_filters.BooleanFilter(widget=BooleanWidget())
    role = CharFieldInFilter(lookup_expr='iexact')
    is_superuser = django_filters.BooleanFilter(widget=BooleanWidget())

    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'verifyed_email', 'role', 'is_superuser')


class BuyerFilter(filters.FilterSet):
    first_name = CharFieldInFilter(lookup_expr='iexact')
    last_name = CharFieldInFilter(lookup_expr='iexact')
    balance_min = django_filters.NumberFilter(field_name='balance', lookup_expr='gt')
    balance_max = django_filters.NumberFilter(field_name='balance', lookup_expr='lt')
    user = CharFieldInFilter(field_name='user__username', lookup_expr='in')

    class Meta:
        model = Buyer
        fields = ('first_name', 'last_name', 'balance', 'user')


class BuyerOfferFilter(filters.FilterSet):
    active_status = CharFieldInFilter(lookup_expr='iexact')

    class Meta:
        model = BuyerOffer
        fields = ('active_status', )


class DealershipFilter(filters.FilterSet):
    name = CharFieldInFilter(lookup_expr='iexact')
    location = CharFieldInFilter(lookup_expr='iexact')
    balance_min = django_filters.NumberFilter(field_name='balance', lookup_expr='gt')
    balance_max = django_filters.NumberFilter(field_name='balance', lookup_expr='lt')

    class Meta:
        model = Dealership
        fields = ('name', 'location', 'balance')


class SupplierFilter(filters.FilterSet):
    name = CharFieldInFilter(lookup_expr='iexact')
    year_of_foundation_min = django_filters.NumberFilter(field_name='year_of_foundation', lookup_expr='gt')
    year_of_foundation_max = django_filters.NumberFilter(field_name='year_of_foundation', lookup_expr='lt')

    class Meta:
        model = Supplier
        fields = ('name', 'year_of_foundation')
