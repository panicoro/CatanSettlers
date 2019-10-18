from rest_framework import serializers
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from catan.models import Room


class RoomSerializer(serializers.ModelSerializer):
    players = serializers.SlugRelatedField(
        many=True,
        queryset=User.objects.all(),
        slug_field='username'
     )
    owner = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()
     )

    class Meta:
        model = Room
        fields = ['id', 'name', 'max_players', 'owner', 'players']

    def update(self, instance, validated_data):
        # Only update the players list...
        players = validated_data.pop('players')
        for player_data in players:
            if not instance.players.filter(username=player_data).exists():
                player = User.objects.filter(username=player_data)[0]
                instance.players.add(player)
        return instance

    def validate_players(self, players):
        # Check if number to put are allowed
        if len(players) > (self.instance.max_players - 1):
            raise serializers.ValidationError("Cannot add more players")
        return players

    def validate(self, data):
        # Check if owner is in players list
        if data['owner'] in data['players']:
            raise serializers.ValidationError(
                "Cannot add the owner to the players")
        return data
