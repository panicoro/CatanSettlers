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
