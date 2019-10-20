from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from catan.models import Board, Game, Hexe
from catan.serializers import (
                                GameListSerializer,
                                BoardSerializer,
                                HexeSerializer
                              )


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
