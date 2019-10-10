from rest_framework import serializers
from catan.models import Card, Player, Last_gained, Resource

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['name']


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['name']



class Last_gainedSerializer(serializers.ModelSerializer):
    resources = ResourceSerializer(read_only=True)
    class Meta:
        model = Last_gained
        fields = ['resources']



class PlayerSerializer(serializers.ModelSerializer):
    settlements = serializers.StringRelatedField(many=True)
    cities = serializers.StringRelatedField(many=True)
    roads = serializers.StringRelatedField(many=True)
    last_gained = Last_gainedSerializer(many=True, read_only=True)

    class Meta:
        model = Player
        fields = ('username', 'colour', 'development_cards',
                'resources_cards', 'settlements', 'cities', 'roads', 'last_gained')