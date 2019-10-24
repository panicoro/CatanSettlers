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
from catan.cargaJson import *



class RoomList(APIView):
    def get(self, request, format=None):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        room = self.get_object(pk)
        room_serializer = RoomSerializer(room)
        room_data = room_serializer.data
        room_data['players'].append(self.request.user)
        serializer = RoomSerializer(room, data=room_data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthAPIView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        data = request.data
        response = {"detail": "Invalid credentials"}

        try:
            data['username'] = data['user']
            data['password'] = data['pass']
        except Exception:
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(username=data['username'],
                            password=data['password'])

        if (user is not None):
            serializer = self.get_serializer(data=request.data)
            response = serializer.validate(request.data)
        else:
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)

        return Response(response, status=status.HTTP_201_CREATED)


class PlayerInfo(APIView):
    def get(self, request, pk):
        game = get_object_or_404(Game, pk=pk)
        user = self.request.user
        player_id = Player.objects.filter(username=user, game=pk).get().id
        queryset_cards = Card.objects.filter(owner=player_id)
        queryset_resource = Resource.objects.filter(owner=player_id)
        serializer_cards = CardSerializer(queryset_cards, many=True)
        serializer_resource = ResourceSerializer(queryset_resource, many=True)
        data = {'resources': serializer_resource.data,
                'cards': serializer_cards.data}
        return Response(data)


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
        player_roads = Road.objects.filter(owner=player.id)
        serialized_roads = RoadSerializer(player_roads, many=True)
        for serialized_road in serialized_roads.data:
            new_road = []
            new_road.append(serialized_road['vertex_1'])
            new_road.append(serialized_road['vertex_2'])
            roads.append(new_road)
        return roads

    def get_settlements(self, player):
        """
        A method to obtain a list of settlements of a player
        Args:
        player: A player object.
        """
        settlements = self.get_list_serialized_objects(
                            queryset=Building.objects.filter(name="SETTLEMENT",
                                                             owner=player.id),
                            serializer=BuildingSerializer, key='position')
        return settlements

    def get_cities(self, player):
        """
        A method to obtain a list of cities of a player
        Args:
        player: A player object.
        """
        cities = self.get_list_serialized_objects(
                            queryset=Building.objects.filter(name="CITY",
                                                             owner=player.id),
                            serializer=BuildingSerializer, key='position')
        return cities

    def get_last_gained(self, player):        
        """
        A method to obtain a list of last_gained of a player
        Args:
        player: A player object.
        """
        last_gained = self.get_list_serialized_objects(
                            queryset=Resource.objects.filter(last_gained=True,
                                                             owner=player.id),
                            serializer=ResourceSerializer, key='resource_name')
        return last_gained

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
            data['roads'] = roads
            data['last_gained'] = last_gained
            data['settlements'] = settlements
            data['cities'] = cities
            serialized_players.append(data)
        return serialized_players

    def throw_dice(self):
        """
        A method to generate a thow of dice
        (uniform discrete distribution)
        """
        return 1 * int(6 * random()) + 1

    def get(self, request, pk):
        game = get_object_or_404(Game, pk=pk)
        # Throw the dices...
        game.current_turn.dices1 = self.throw_dice()
        game.current_turn.dices2 = self.throw_dice()
        game.save()
        # Get the game serializer...
        serialized_game = GameSerializer(game)
        data = serialized_game.data
        # Change data presentation of a dices
        dices1 = data['current_turn'].pop('dices1')
        dices2 = data['current_turn'].pop('dices2')
        data['current_turn']['dices'] = [dices1, dices2]
        # Add players...
        serialized_players = self.get_players(pk=pk)
        data['players'] = serialized_players
        return Response(data)


class GameList(APIView):
    def get(self, request, format=None):
        games = Game.objects.all()
        games_serializers = GameListSerializer(games, many=True)
        return Response(games_serializers.data)


class BoardList(APIView):
    def get(self, request, format=None):
        boards = Board.objects.all()
        boards_serializers = BoardSerializer(boards, many=True)
        return Response(boards_serializers.data)


class BoardInfo(APIView):
    def get(self, request, pk):
        game = get_object_or_404(Game, pk=pk)
        board_hexes = Hexe.objects.filter(board=game.board.id)
        hexes_serializer = HexeSerializer(board_hexes, many=True)
        return Response({"hexes": hexes_serializer.data})


class BuiltRoad(APIView):
    def post(self, request, pk):
        data = request.data
        game = get_object_or_404(Game, pk=pk)
        user = self.request.user
        owner = Player.objects.filter(username=user, game=pk).get()
        level1 = int(data['payload']['level1'])
        index1 = int(data['payload']['index1'])
        level2 = int(data['payload']['level2'])
        index2 = int(data['payload']['index2'])
        position_1 = VertexPosition.objects.filter(level=level1, index=index1).get()
        position_2 = VertexPosition.objects.filter(level=level2, index=index2).get()
        list_all_road = Road.objects.filter(game=pk)
        position_road = CheckPositionRoad(list_all_road,level1,index1,level2,index2)
        #verifico si la posicion esta libre
        if position_road:
            response = {"detail": "invalid position, reserved"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        resources = Resource.objects.filter(owner=owner.id, game=pk)
        list_resources = ResourcesRoad(resources)
        # verifico recursos necesarios
        if len(list_resources) != 2:
            response = {"detail": "Doesn't have enough resources"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        roads = Road.objects.filter(owner=owner.id, game=pk)
        is_roads= CheckRoads_Road(roads, level1, index1, level2, index2)
        buildings = Building.objects.filter(owner=owner.id, game=pk)
        is_building = CheckBuild_Road(buildings,level1,index1,level2,index2)
        #verifico que tenga camino o edificio propio
        if not is_roads and not is_building:
            response = {"detail": "invalid position"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        deleteResource(resources)
        new_road = Road(game=game, vertex_1=position_1, vertex_2=position_2, owner=owner)
        new_road.save()
        return Response(status=status.HTTP_200_OK)