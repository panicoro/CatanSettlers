from rest_framework import serializers
from catan.models import VertexPosition, Hexes, Board, Game

class VertexPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VertexPosition
        fields = ['level', 'index']

class HexesSerializer(serializers.ModelSerializer):
    position = VertexPositionSerializer()
    class Meta:
        model = Hexes
        fields = ['position','terrain', 'token']

class BoardSerializer(serializers.ModelSerializer):
    hexes = HexesSerializer(many=True)
    class Meta:
        model = Board
        fields = ['name', 'hexes']

class GameListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'name']

