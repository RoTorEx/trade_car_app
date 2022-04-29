from rest_framework import serializers

from supplier.models import Supplier, SupplierHistory
from user.models import UserProfile


class UserSupplierSerializer(serializers.ModelSerializer):
    '''Supplier user serializer.'''
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'role', 'email', 'verifyed_email', 'is_superuser']


class SupplierSerializer(serializers.ModelSerializer):
    '''Supplier serializer.'''
    user = UserSupplierSerializer(read_only=True)

    class Meta:
        model = Supplier
        fields = ['id', 'user', 'name', 'year_of_foundation', 'cars', 'cars_price', 'cars_chars', 'is_active']


class SupplierHistorySerializer(serializers.ModelSerializer):
    '''Delivery history serializer.'''
    class Meta:
        model = SupplierHistory
        fields = '__all__'
