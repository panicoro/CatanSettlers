from rest_framework import serializers
from django.contrib.auth.models import User
from catan.models import Room


class RoomSerializer(serializers.ModelSerializer):
    players = serializers.StringRelatedField(many=True)
    owner = serializers.StringRelatedField()                                              
    class Meta:
        model = Room
        fields = ['id', 'name', 'max_players', 'owner', 'players']
