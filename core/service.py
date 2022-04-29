import django_filters
from django_filters import rest_framework as filters
from django_filters.widgets import BooleanWidget

from user.models import UserProfile


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
