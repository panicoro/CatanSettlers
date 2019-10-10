from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from catan.models import Board, Hexes, Game
from catan.serializers import BoardSerializer, HexesSerializer, GameSerializer

@api_view(['GET'])
def list_board(request, format=None):

    if request.method == 'GET':
        boards = Board.objects.all()
        serializer = BoardSerializer(boards, many=True)
        return Response(serializer.data)

@api_view(['GET'])             
def board_detail(request, pk, format=None):

    try:
        board = Board.objects.get(pk=pk)
    except BoardSerializer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BoardSerializer(board)
        return Response(serializer.data)

@api_view(['GET'])
def list_game(request, format=None):

    if request.method == 'GET':
        game = Game.objects.all()
        serializer = GameSerializer(game, many=True)
        return Response(serializer.data)

@api_view(['GET'])             
def game_detail(request, pk, format=None):
    try:
        game = Game.objects.get(pk=pk)
    except Game.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GameSerializer(game)
        return Response(serializer.data)

@api_view(['GET'])
def list_hexes(request, format=None):

    if request.method == 'GET':
        hexes = Hexes.objects.all()
        serializer = HexesSerializer(hexes, many=True)
        return Response(serializer.data)

