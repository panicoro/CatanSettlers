from rest_framework import serializers
from catan.models import HexePosition, Hexe, Board, Game


class HexePositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HexePosition
        fields = ['level', 'index']


class HexeSerializer(serializers.ModelSerializer):
    position = HexePositionSerializer()

    class Meta:
        model = Hexe
        fields = ['position', 'terrain', 'token']


class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ['id', 'name']


class GameListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'name', 'board']
