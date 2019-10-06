from rest_framework import serializers
from catan.models import Tablero, Hexagono, Vertice

class TableroSerializer(serializers.ModelSerializer):
    hexagonos = serializers.StringRelatedField(many=True)
    vertices = serializers.StringRelatedField(many=True)
    class Meta:
        model = Tablero
        fields = ['id', 'nombre', 'vertices', 'hexagonos']

    def create(selef, validated_data):
        return Tablero.objects.create(**validated_data)

class HexagonoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hexagono
        fields = ['id', 'resource', 'token']
    def create(selef, validated_data):
        return Hexagono.objects.create(**validated_data)

class VerticeSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Vertice
        fields = ['id', 'nivel', 'indice']

    def create(selef, validated_data):
        return Vertice.objects.create(**validated_data)