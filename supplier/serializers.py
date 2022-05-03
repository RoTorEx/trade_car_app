from rest_framework import serializers

from supplier.models import Supplier, SupplierGarage
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
        fields = ['id', 'user', 'name', 'year_of_foundation', 'is_active']


class SupplierGarageSerializer(serializers.ModelSerializer):
    '''Supplier's garage serializer.'''
    class Meta:
        model = SupplierGarage
        fields = '__all__'
