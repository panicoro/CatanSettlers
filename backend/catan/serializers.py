from rest_framework import serializers
from catan.models import Card, Player, Resource


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['card_name']


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['resource_name']
