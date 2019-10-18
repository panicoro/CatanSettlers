from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import fields
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.reverse import reverse as api_reverse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.six import text_type
from catan.models import Room, Card, Player, Resource


class SignupSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super(SignupSerializer, cls).get_token(user)
        return token

    def validate(self, attrs):
        user = authenticate(username=attrs['username'],
                            password=attrs['password'])
        data = {}
        data['username'] = user.username
        data['email'] = user.email
        refresh = self.get_token(user)
        data['token'] = text_type(refresh)
        data['refresh'] = text_type(refresh)
        data['access'] = text_type(refresh.access_token)
        return data


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


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['card_name']


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['resource_name']
