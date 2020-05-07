from rest_framework import status
from rest_framework.views import APIView
from catan.serializers import *
from django.http import Http404
from random import random
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from catan.models import *


class RoomList(APIView):
    def get(self, request, format=None):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        data = request.data
        data['owner'] = request.user
        data['players'] = [request.user.username]
        data['game_has_started'] = False
        serializer = RoomSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            data.pop('board_id')
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)


class RoomDetail(APIView):
    def get(self, request, pk, format=None):
        room = get_object_or_404(Room, pk=pk)
        room_serializer = RoomSerializer(room)
        data = room_serializer.data
        data.pop('board_id')
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        room = get_object_or_404(Room, pk=pk)
        room_serializer = RoomSerializer(room)
        room_data = room_serializer.data
        room_data['players'].append(request.user.username)
        serializer = RoomSerializer(room, data=room_data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        room = get_object_or_404(Room, pk=pk)
        if room.is_full():
            room.start_game()
            return Response(status=status.HTTP_204_NO_CONTENT)
        data = {"detail": "Can't start the game without all players"}
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = request.user
        room = get_object_or_404(Room, pk=pk)
        if room.can_delete(user):
            room.delete()
            return Response(
                status=status.HTTP_204_NO_CONTENT)
        data = {"detail": "Can't delete the room"}
        return Response(data, status=status.HTTP_403_FORBIDDEN)
