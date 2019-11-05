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
from random import random, randint
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from catan.models import *
from catan.cargaJson import *
from catan.dices import throw_dices
from rest_framework.permissions import AllowAny
from random import shuffle
from catan.views.actions.road import build_road
from catan.views.actions.build import build_settlement
from catan.views.actions.robber import move_robber
from catan.views.actions.play_cards import move_robberCard


class PlayerInfo(APIView):
    def get(self, request, pk):
        resource_list = []
        card_list = []
        game = get_object_or_404(Game, pk=pk)
        user = self.request.user
        player_id = Player.objects.filter(username=user, game=pk).get().id
        queryset_card = Card.objects.filter(owner=player_id)
        queryset_resource = Resource.objects.filter(owner=player_id)
        serializer_card = CardSerializer(queryset_card, many=True)
        serializer_resource = ResourceSerializer(queryset_resource, many=True)
        for resource in serializer_resource.data:
            resource_list.append(resource['resource_name'])
        for card in serializer_card.data:
            card_list.append(card['card_name'])
        data = {'resources': resource_list,
                'cards': card_list}
        return Response(data)


class PlayerActions(APIView):
    def check_player_in_turn(self, game, player):
        """
        A method to check if the player is in turn in the given game.
        Args:
        @game: a started game.
        @player: a player in the game.
        """
        return game.current_turn.user == player.username

    """def Road(self, game, player, level1, index1, level2, index2):
        position_1 = VertexPosition.objects.filter(level=level1,
                                                   index=index1).get()
        position_2 = VertexPosition.objects.filter(level=level2,
                                                   index=index2).get()
        new_road = Road(game=game, vertex_1=position_1,
                        vertex_2=position_2, owner=player)
        new_road.save()
    """

    def post(self, request, pk):
        data = request.data
        game = get_object_or_404(Game, pk=pk)
        player = get_object_or_404(Player, username=request.user, game=game)
        my_user = request.user
        my_player = Player.objects.get(username=my_user, game=game)
        # Check if the player is on his turn
        if not self.check_player_in_turn(game, player):
            response = {"detail": "Not in turn"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        if data['type'] == 'build_settlement':
            response = build_settlement(data['payload'], game, player)
            return response
        user = self.request.user
        owner = Player.objects.filter(username=user, game=pk).get()
        if data['type'] == 'build_road':
            response = build_road(data['payload'], game, owner)
            return response

        if data['type'] == 'move_robber':
            response = move_robber(data['payload'], game, my_user, my_player)
            return response

        if data['type'] == 'play_knight_card':
            response = move_robberCard(data['payload'], game, my_user, my_player)
            return response

        response = {"detail": 'Please select a valid action'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
