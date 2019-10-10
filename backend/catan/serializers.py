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
        # Only update the players list...
        self.instance.players.clear()
        players = validated_data.pop('players')
        for player_data in players:
            username = player_data.pop('username')
            player = User.objects.filter(username=username)[0]
            instance.players.add(player)
        return instance

    def validate_owner(self, value):
        # Owner of the room must be the same
        instance = self.instance
        if instance.owner.username != value['username']:
            raise serializers.ValidationError("Cannot change owner")
        return value

    def validate_max_players(self, value):
        # Maximum number of players must be the same
        if self.instance.max_players != value:
            raise serializers.ValidationError("Cannot change max players")
        return value

    def validate_name(self, value):
        # Name must be the same
        if self.instance.name != value:
            raise serializers.ValidationError("Cannot change name")
        return value

    def validate_players(self, players):
        # Check repeated player dictionaries
        seen = set()
        for player in players:
            tup_player = tuple(player.items())
            if tup_player in seen:
                raise serializers.ValidationError("Players has repeat dicts")
            else:
                seen.add(tup_player)
        # Check if players are registered users
        for player in players:
            if not User.objects.filter(username=player['username']).exists():
                raise serializers.ValidationError(
                    "Cannot add a non register user")
        # Check if number to put are allowed
        if len(players) > (self.instance.max_players - 1):
            raise serializers.ValidationError("Too many players to add")
        return players

    def validate(self, data):
        # Check if owner is in players list
        if data['owner'] in data['players']:
            raise serializers.ValidationError(
                "Cannot add the owner to the players")
        return data
