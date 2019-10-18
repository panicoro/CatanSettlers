from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from catan.models import Board, Game
from catan.serializers import GameListSerializer, BoardSerializer

class GameList(APIView):
    def get(self, requests, format=None):
        games = Game.objects.all()
        gamesserializers = GameListSerializer(games, many=True)
        return Response(gamesserializers.data)

class BoardInfo(APIView):
    def get(self, request, pk):
        board = get_object_or_404(Board, pk=pk)
        board = Board.objects.get(pk=pk)
        serializer_board = BoardSerializer(board)
        return Response(serializer_board.data)