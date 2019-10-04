from rest_framework import serializers
from django.contrib.auth.models import User
from catan.models import Room


class UserSerializer(serializers.ModelSerializer):
    rooms = serializers.PrimaryKeyRelatedField(many=True,
                                               queryset=Room.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'rooms']


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'name', 'max_players', 'owner', 'players']
