from rest_framework import serializers

from dealership.models import Dealership, DealershipHistory


class DealershipSerializer(serializers.ModelSerializer):
    '''Car dealership serializer.'''
    class Meta:
        model = Dealership
        fields = '__all__'


class DealershipHistorySerializer(serializers.ModelSerializer):
    '''Car showroom history serializer.'''
    class Meta:
        model = DealershipHistory
        fields = '__all__'
