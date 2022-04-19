from rest_framework import serializers

from .models import *


class DealershipSerializer(serializers.ModelSerializer):
    '''Сериализатор автосалонов.'''
    class Meta:
        model = Dealership
        fields = '__all__'


class DealershipHistorySerializer(serializers.ModelSerializer):
    '''Сериализатор истории автосалонов.'''
    class Meta:
        model = DealershipHistory
        fields = '__all__'
