from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import fields
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.reverse import reverse as api_reverse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.utils.six import text_type
from catan.models import *
from django.core.exceptions import ValidationError


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
        fields = ['id', 'name', 'max_players', 'owner', 'players',
                  'game_has_started', 'game_id', 'board_id']

    def create(self, validaded_data):
        players = validaded_data.pop('players')
        new_room = Room.objects.create(**validaded_data)
        new_room.save()
        new_room.players.set(players)
        return new_room

    def update(self, instance, validated_data):
        # Only update the players list...
        players = validated_data.pop('players')
        for player_data in players:
            if not instance.players.filter(username=player_data).exists():
                player = User.objects.filter(username=player_data)[0]
                instance.players.add(player)
        return instance

    def validate_board_id(self, board_id):
        if not Board.objects.filter(id=board_id).exists():
            raise serializers.ValidationError("Cannot add this board")
        return board_id

    def validate_players(self, players):
        # Check if number to put are allowed
        if len(players) > 3:
            raise serializers.ValidationError("Cannot add more players")
        return players

    def validate(self, data):
        # Check if owner is in players list
        if data['owner'] in data['players']:
            raise serializers.ValidationError(
                "Cannot add the owner to the players")
        return data


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['card_name']


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['resource_name']


class HexePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HexePosition
        fields = ['level', 'index']


class HexeSerializer(serializers.ModelSerializer):
    position = HexePositionSerializer()

    class Meta:
        model = Hexe
        fields = ['position', 'terrain', 'token']


class VertexPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VertexPosition
        fields = ['level', 'index']


class RoadSerializer(serializers.ModelSerializer):
    vertex_1 = VertexPositionSerializer()
    vertex_2 = VertexPositionSerializer()

    class Meta:
        model = Road
        fields = ['vertex_1', 'vertex_2']


class BuildingSerializer(serializers.ModelSerializer):
    position = VertexPositionSerializer()

    class Meta:
        model = Building
        fields = ['position']


class PlayerSerializer(serializers.ModelSerializer):
    username = serializers.SlugRelatedField(queryset=User.objects.all(),
                                            slug_field='username')

    class Meta:
        model = Player
        fields = ['username', 'colour', 'victory_points']


class Current_TurnSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(queryset=User.objects.all(),
                                        slug_field='username')

    class Meta:
        model = Current_Turn
        fields = ['user', 'dices1', 'dices2']


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'name']


class GameListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = ['id', 'name']


class GameSerializer(serializers.ModelSerializer):
    current_turn = Current_TurnSerializer()
    robber = HexePositionSerializer()
    winner = serializers.SlugRelatedField(queryset=User.objects.all(),
                                          slug_field='username')

    class Meta:
        model = Game
        fields = ['robber', 'current_turn', 'winner']
