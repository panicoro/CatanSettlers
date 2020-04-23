from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from rest_framework import fields, serializers
from rest_framework.validators import UniqueValidator
from rest_framework.reverse import reverse as api_reverse
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from catan.models import *
from six import text_type


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
        if len(players) > 4:
            raise serializers.ValidationError("Cannot add more players")
        return players


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['card_name']


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['name']


class HexeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hexe
        fields = ['level', 'index', 'terrain', 'token']


class RoadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Road
        fields = ['level_1', 'level_2', 'index_1', 'index_2']


class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ['level', 'index']


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
    winner = serializers.SlugRelatedField(queryset=User.objects.all(),
                                          slug_field='username')
    robber = HexeSerializer()

    class Meta:
        model = Game
        fields = ['robber', 'current_turn', 'winner']
