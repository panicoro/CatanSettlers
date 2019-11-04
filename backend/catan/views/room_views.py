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
from catan.dices import throw_dices
from django.http import Http404
from random import random
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from catan.models import *
from catan.cargaJson import *
from catan.dices import throw_dices
from rest_framework.permissions import AllowAny
from random import shuffle
from django.db.models import Q


class RoomList(APIView):
    def get(self, request, format=None):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        data['owner'] = request.user
        data['players'] = []
        data['game_has_started'] = False
        serializer = RoomSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            data.pop('board_id')
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RoomDetail(APIView):
    def get_object(self, pk):
        try:
            return Room.objects.get(pk=pk)
        except Room.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        room = get_object_or_404(Room, pk=pk)
        room_serializer = RoomSerializer(room)
        data = room_serializer.data
        data.pop('board_id')
        return Response(data, status=status.HTTP_200_OK)

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

    def patch(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        board = get_object_or_404(Board, id=room.board_id)
        vertex_positions = VertexPosition.objects.all()
        hexes = Hexe.objects.filter(board=board)
        desert_terrain = hexes.filter(terrain="desert")[0]
        desert_pos = desert_terrain.position
        players = room.players.all()
        if (len(players) == 3):
            game = Game.objects.create(name=room.name, board=board,
                                       robber=desert_pos)
            turns = [1, 2, 3, 4]
            shuffle(turns)
            player1 = Player.objects.create(turn=turns[0], username=room.owner,
                                            game=game, colour="blue")
            player2 = Player.objects.create(turn=turns[1], username=players[0],
                                            game=game, colour="red")
            player3 = Player.objects.create(turn=turns[2], username=players[1],
                                            game=game, colour="yellow")
            player4 = Player.objects.create(turn=turns[3], username=players[2],
                                            game=game, colour="green")
            first_player = Player.objects.filter(game=game, turn=1)[0]
            current_turn = Current_Turn.objects.create(
                game=game,
                user=first_player.username)
            room.game_has_started = True
            room.game_id = game.id
            room.save()
            building1 = Building.objects.create(
                name="settlement", game=game,
                owner=player1, position=vertex_positions[0])
            building2 = Building.objects.create(
                name="settlement", game=game,
                owner=player2, position=vertex_positions[1])
            building3 = Building.objects.create(
                name="settlement", game=game,
                owner=player3, position=vertex_positions[2])
            building4 = Building.objects.create(
                name="settlement", game=game,
                owner=player4, position=vertex_positions[3])
            throw_dices(game, current_turn, board)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            ValidationError("Can't start the game without all players"),
            status=status.HTTP_400_BAD_REQUEST)
