from catan.models import *
from rest_framework import serializers


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['resource_name']


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['card_name']
