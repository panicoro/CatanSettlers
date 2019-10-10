from rest_framework import serializers
from catan.models import Board, Hexes, Vertex, VertexPosition,Game

class HexesSerializer(serializers.ModelSerializer):
    position = serializers.CharField(source='get_position_display')
    class Meta:
        model = Hexes
        fields = ['position', 'resource', 'token']
    def create(selef, validated_data):
        return Hexes.objects.create(**validated_data)

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'name', 'in_turn']

class VertexSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Vertex
        fields = ['id', 'level', 'index']

    def create(selef, validated_data):
        return Vertex.objects.create(**validated_data)

class BoardSerializer(serializers.ModelSerializer):
    hexes = serializers.StringRelatedField(many=True)
    #vertices = serializers.StringRelatedField(many=True)
    #games = serializers.StringRelatedField(many=True)
    class Meta:
        model = Board
        fields = ['id', 'name', 'hexes']

    def create(selef, validated_data):
        return Board.objects.create(**validated_data)

class VertexPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VertexPosition
        fields = ['level', 'index']


