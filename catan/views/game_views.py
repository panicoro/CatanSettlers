from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt import authentication
from catan.serializers import *
from django.http import Http404
from random import random
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from catan.models import *
from rest_framework.permissions import AllowAny
from random import shuffle
from django.db.models import Q


class GameInfo(APIView):
    def get_list_without_keys(self, serialized_list, key):
        """
        A method to quit the keys of the serialized objects
        Args:
        serialized_list: serialized list of objects.
        key: a key to obtain the elements.
        """
        data = []
        for serialized_data in serialized_list.data:
            data.append(serialized_data[key])
        return data

    def get_list_serialized_objects(self, queryset, serializer, key):
        """
        A method to get serialized objects without keys from a queryset
        Args:
        queryset: a queryset of certain objects.
        key: a key to obtain elements.
        """
        data = []
        serialized_objects = serializer(queryset, many=True)
        final_data = self.get_list_without_keys(serialized_objects, key)
        return final_data

    def get_roads(self, player):
        """
        A method to obtain a list of roads of a player
        Args:
        player: A player object.
        """
        roads = []
        player_roads = Road.objects.filter(owner=player)
        serialized_roads = RoadSerializer(player_roads, many=True)
        for serialized_road in serialized_roads.data:
            new_road = []
            vertex_1 = {'level': serialized_road['level_1'],
                        'index': serialized_road['index_1']}
            vertex_2 = {'level': serialized_road['level_2'],
                        'index': serialized_road['index_2']}
            new_road.append(vertex_1)
            new_road.append(vertex_2)
            roads.append(new_road)
        return roads

    def get_settlements(self, player):
        """
        A method to obtain a list of settlements of a player
        Args:
        player: A player object.
        """
        settlements = Building.objects.filter(name="settlement", owner=player)
        serializered = BuildingSerializer(settlements, many=True)
        return serializered.data

    def get_cities(self, player):
        """
        A method to obtain a list of cities of a player
        Args:
        player: A player object.
        """
        cities = Building.objects.filter(name="city", owner=player)
        serializered = BuildingSerializer(cities, many=True)
        return serializered.data

    def get_last_gained(self, player):
        """
        A method to obtain a list of last_gained of a player
        Args:
        player: A player object.
        """
        last_gained = self.get_list_serialized_objects(
                            queryset=Resource.objects.filter(last_gained=True,
                                                             owner=player.id),
                            serializer=ResourceSerializer, key='name')
        return last_gained

    def get_resource_card(self, player, game):
        """
        """
        resource_card = Resource.objects.filter(Q(owner=player) &
                                                (Q(name='ore') |
                                                 Q(name='brick') |
                                                 Q(name='lumber') |
                                                 Q(name='grain') |
                                                 Q(name='wool'))).count()
        return resource_card

    def get_development_card(self, player, game):
        """
        """
        development_card = Card.objects.filter(Q(owner=player) &
                                               (Q(name='knight') |
                                                Q(name='monopoly') |
                                                Q(name='year_of_plenty') |
                                                Q(name='road_building') |
                                                Q(name='victory_point'))
                                               ).count()
        return development_card

    def get_players(self, pk):
        """
        A method to obtain the list of serialized players
        """
        players = Player.objects.filter(game=pk)
        serialized_players = []
        for player in players:
            partial_serialized_player = PlayerSerializer(player)
            data = partial_serialized_player.data
            last_gained = self.get_last_gained(player)
            settlements = self.get_settlements(player)
            cities = self.get_cities(player)
            roads = self.get_roads(player)
            resource_card = self.get_resource_card(player, pk)
            development_card = self.get_development_card(player, pk)
            data['resources_cards'] = resource_card
            data['development_cards'] = development_card
            data['roads'] = roads
            data['last_gained'] = last_gained
            data['settlements'] = settlements
            data['cities'] = cities
            serialized_players.append(data)
        return serialized_players

    def get(self, request, pk):
        game = get_object_or_404(Game, pk=pk)
        # Get the game serializer...
        serialized_game = GameSerializer(game)
        data = serialized_game.data
        # Change data presentation of a dices
        data['robber'].pop('terrain')
        data['robber'].pop('token')
        dices1 = data['current_turn'].pop('dices1')
        dices2 = data['current_turn'].pop('dices2')
        data['current_turn']['dice'] = [dices1, dices2]
        # Add players...
        serialized_players = self.get_players(pk=pk)
        data['players'] = serialized_players
        return Response(data)


class GameList(APIView):
    def get(self, request, format=None):
        games = Game.objects.all()
        games_serializers = GameListSerializer(games, many=True)
        data = []
        for serialized_game in games_serializers.data:
            game_data = serialized_game
            game_id = game_data['id']
            current_turn = Current_Turn.objects.filter(game=game_id)[0]
            game_data['in_turn'] = current_turn.user.username
            data.append(game_data)
        return Response(data)
