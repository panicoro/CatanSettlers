from rest_framework import serializers
from catan.models import Tablero, Hexagono, Vertice, VertexPosition

class HexagonoSerializer(serializers.ModelSerializer):
    position = serializers.CharField(source='get_position_display')
    class Meta:
        model = Hexagono
        fields = ['position', 'resource', 'token']  #si saco un campo , entonces no se mostrara en la pagina
    def create(selef, validated_data):
        return Hexagono.objects.create(**validated_data)

class VerticeSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Vertice
        fields = ['id', 'nivel', 'indice']

    def create(selef, validated_data):
        return Vertice.objects.create(**validated_data)

class TableroSerializer(serializers.ModelSerializer):
    hexagonos = serializers.StringRelatedField(many=True)
    vertices = serializers.StringRelatedField(many=True)
    class Meta:
        model = Tablero
        fields = ['id', 'nombre', 'vertices', 'hexagonos']

    def create(selef, validated_data):
        return Tablero.objects.create(**validated_data)


class VertexPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VertexPosition
        fields = ['level', 'index']


