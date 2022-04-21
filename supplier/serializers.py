from rest_framework import serializers

from supplier.models import Supplier, SupplierHistory


class SupplierSerializer(serializers.ModelSerializer):
    '''Supplier serializer.'''
    class Meta:
        model = Supplier
        fields = '__all__'


class SupplierHistorySerializer(serializers.ModelSerializer):
    '''Delivery history serializer.'''
    class Meta:
        model = SupplierHistory
        fields = '__all__'
