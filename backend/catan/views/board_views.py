from rest_framework.views import APIView
from catan.serializers import BoardSerializer, HexeSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from catan.models import Board, Hexe, Game


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
        hexes = hexes_serializer.data
        for hexe in hexes:
            hexe['position'] = {'level': hexe['level'], 
                                'index': hexe['index']}
            hexe.pop('level')
            hexe.pop('index')
        return Response({"hexes": hexes})
