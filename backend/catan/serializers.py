from rest_framework import serializers
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from catan.models import Room


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()],
            }
        }


class RoomSerializer(serializers.ModelSerializer):
    players = UserSerializer(many=True)
    owner = UserSerializer()

    class Meta:
        model = Room
        fields = ['id', 'name', 'max_players', 'owner', 'players']

    def update(self, instance, validated_data):
        owner_data = validated_data.pop('owner')
        username = owner_data.pop('username')
        owner = get_user_model().objects.get_or_create(
            username=username)[0]
        instance.owner = owner
        players = validated_data.pop('players')
        for player_data in players:
            username = player_data.pop('username')
            player = get_user_model().objects.get_or_create(
                username=username)[0]
            instance.players.add(player)
        instance.max_players = validated_data['max_players']
        instance.name = validated_data['name']
        return instance
