from django.contrib.auth.models import User
from .models import Game, Resource,Player
from rest_framework import serializers
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']
        extra_kwargs = {
            'username': {
                'validators': [UnicodeUsernameValidator()],
            }
        }

class PlayerSerializer(serializers.ModelSerializer):
    username = UserSerializer()
    class Meta:
        model = Player
        fields = ['username','game']

class GameSerializer(serializers.ModelSerializer):
    players = serializers.StringRelatedField(many=True)
    class Meta:
        model = Game
        fields = ('auto_id','name', 'players')

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ['id','name']