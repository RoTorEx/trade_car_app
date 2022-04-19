from rest_framework import serializers

from .models import *


class SupplierSerializer(serializers.ModelSerializer):
    '''Сериализатор поставщиков.'''
    class Meta:
        model = Supplier
        fields = '__all__'


class SupplierHistorySerializer(serializers.ModelSerializer):
    '''Сериализатор истории поставщиков.'''
    class Meta:
        model = SupplierHistory
        fields = '__all__'
