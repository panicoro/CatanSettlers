from rest_framework.views import APIView
from django.contrib.auth.models import User
from catan.serializers import *
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from catan.models import *
from catan.cargaJson import *
from catan.dices import throw_dices
from rest_framework.permissions import AllowAny
from random import shuffle
from catan.views.actions.road import (
                    build_road, canBuild_Road,
                    posiblesRoads,
                    posiblesRoads_cardRoadBuilding,
                    play_road_building_card
                )
from catan.views.actions.buy_card import buy_card
from catan.views.actions.build import (
            build_settlement, canBuild_Settlement,
            posiblesSettlements)
from catan.views.actions.bank import bank_trade
from catan.views.actions.robber import (
                move_robber, get_sum_dices,
                posiblesRobberPositions
            )
from catan.views.actions.play_cards import move_robberCard
from catan.views.actions.change_turn import change_turn


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

    def get_roads(self, posibles_roads, item):
        """
        A function to get the payload in a given item with the positions
        available to build roads.
        Args:
        @posibles_roads = a list of [vertex_position, vertex_position]
        that represent the posibles roads to build.
        @item = a given item to push in the data
        """
        for road in posibles_roads:
            new_road = []
            new_road.append(VertexPositionSerializer(road[0]).data)
            new_road.append(VertexPositionSerializer(road[1]).data)
            item['payload'].append(new_road)
        return item
            
    def get(self, request, pk):
        game = get_object_or_404(Game, pk=pk)
        user = request.user
        player = get_object_or_404(Player, username=user, game=game)
        data = []
        if canBuild_Road(player):
            item = {"type": 'build_road'}
            posibles_roads = posiblesRoads(player)
            item['payload'] = []
            item = self.get_roads(posibles_roads, item) 
            if len(item['payload']) != 0:
                data.append(item)
        if canBuild_Settlement(player):
            item = {"type": 'build_settlement'}
            posibles_setlements = posiblesSettlements(player)
            serialized_positions = VertexPositionSerializer(
                                        posibles_setlements,
                                        many=True)
            item['payload'] = serialized_positions.data
            if len(item['payload']) != 0:
                data.append(item)
        if sum(get_sum_dices(game)) == 7:
            item = {"type": 'move_robber'}
            posibles_robber = posiblesRobberPositions(game)
            item["payload"] = posibles_robber
            data.append(item)
        if Card.objects.filter(owner=player,
                               card_name='knight').exists():
            item = {"type": 'play_knight_card'}
            posibles_robber = posiblesRobberPositions(game)
            item["payload"] = posibles_robber
            data.append(item)
        if Card.objects.filter(owner=player,
                               card_name='road_building').exists():
            item = {"type": 'play_road_building_card'}
            posibles_roads = posiblesRoads_cardRoadBuilding(player)
            item['payload'] = []
            item = self.get_roads(posibles_roads, item)
            if len(item['payload']) != 0:
                data.append(item)
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request, pk):
        data = request.data
        game = get_object_or_404(Game, pk=pk)
        user = request.user
        player = get_object_or_404(Player, username=user, game=game)
        # Check if the player is on his turn
        if not self.check_player_in_turn(game, player):
            response = {"detail": "Not in turn"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        if data['type'] == 'end_turn':
            change_turn(game)
            throw_dices(game)
            return Response(status=status.HTTP_204_NO_CONTENT)
        if data['type'] == 'build_settlement':
            response = build_settlement(data['payload'], game, player)
            return response
        if data['type'] == 'build_road':
            response = build_road(data['payload'], game, player)
            return response
        if data['type'] == 'buy_card':
            response = buy_card(game, player)
            return response
        if data['type'] == 'bank_trade':
            response = bank_trade(data['payload'], game, player)
            return response
        if data['type'] == 'move_robber':
            response = move_robber(data['payload'], game, user, player)
            return response
        if data['type'] == 'play_knight_card':
            response = move_robberCard(data['payload'], game, user,
                                       player)
            return response
        if data['type'] == 'play_road_building_card':
            response = play_road_building_card(data['payload'], game, player)
            return response
        response = {"detail": 'Please select a valid action'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
