from rest_framework.views import APIView
from django.contrib.auth.models import User
from catan.serializers import *
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from catan.models import *
from catan.dices import throw_dices
from rest_framework.permissions import AllowAny
from random import shuffle
from catan.views.actions.road import (
            build_road,
            posibles_roads_card_road_building,
            play_road_building_card)
from catan.views.actions.buy_card import buy_card, can_buy_card
from catan.views.actions.bank import bank_trade, can_trade_with_bank
from catan.views.actions.robber import (
                move_robber, get_sum_dices,
                posiblesRobberPositions
            )
from catan.views.actions.build import build_settlement
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
            resource_list.append(resource['name'])
        for card in serializer_card.data:
            card_list.append(card['card_name'])
        data = {'resources': resource_list,
                'cards': card_list}
        return Response(data)


class PlayerActions(APIView):

    def to_json_positions(self, list_positions):
        data = []
        for position in list_positions:
            data.append({'level': position[0],
                         'index': position[1]})
        return data

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
            # new_road.append(VertexPositionSerializer(road[0]).data)
            # new_road.append(VertexPositionSerializer(road[1]).data)
            item['payload'].append(new_road)
        return item

    def get(self, request, pk):
        game = get_object_or_404(Game, pk=pk)
        user = request.user
        player = get_object_or_404(Player, username=user, game=game)
        turn = Current_Turn.objects.get(game=game)
        data = []
        if not self.check_player_in_turn(game, player):
            return Response(data, status=status.HTTP_200_OK)
        game_stage = game.current_turn.game_stage
        last_action = game.current_turn.last_action
        # Las acciones posibles cambian si estan en la fase de construccion
        # Si un jugador esta al comienzo de su fase, se le muestran las
        # opciones para construir un poblado, luego las para construir
        # una carretera luego debe terminar el turno no puede hacer nada mas...
        if game_stage != 'FULL_PLAY':
            if last_action == 'NON_BLOCKING_ACTION':
                item = {"type": 'build_settlement'}
                item['payload'] = game.posibles_initial_settlements()
                data.append(item)
            if last_action == 'BUILD_SETTLEMENT':
                item = {"type": 'build_road'}
                item['payload'] = posibles_initial_roads(player)
                data.append(item)
            if last_action == 'BUILD_ROAD':
                item = {"type": 'end_turn'}
                data.append(item)
            return Response(data, status=status.HTTP_200_OK)
        else:
            if sum(get_sum_dices(game)) == 7 and not turn.robber_moved:
                item = {"type": 'move_robber'}
                posibles_robber = posiblesRobberPositions(game)
                item["payload"] = posibles_robber
                data.append(item)
                return Response(data, status=status.HTTP_200_OK)
            else:
                item = {"type": 'end_turn'}
                data.append(item)
                if player.has_necessary_resources('build_road'):
                    item = {"type": 'build_road'}
                    posibles_roads = player.posible_roads()
                    item['payload'] = []
                    for road in posibles_roads:
                        item['payload'].append(self.to_json_positions(road))
                    if len(item['payload']) != 0:
                        data.append(item)
                if can_trade_with_bank(game, player):
                    item = {"type": 'bank_trade'}
                    data.append(item)
                if can_buy_card(game, player):
                    item = {"type": 'buy_card'}
                    data.append(item)
                if player.has_necessary_resources('build_settlement'):
                    item = {"type": 'build_settlement'}
                    posibles_settlements = player.posibles_settlements()
                    item['payload'] = self.to_json_positions(
                                        posibles_settlements)
                    if len(item['payload']) != 0:
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
                    posibles_roads = posibles_roads_card_road_building(player)
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
        game_stage = game.current_turn.game_stage
        # Check if the player is on his turn
        if not self.check_player_in_turn(game, player):
            response = {"detail": "Not in turn"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        if data['type'] == 'end_turn':
            turn = Current_Turn.objects.get(game=game)
            if sum(get_sum_dices(game)) == 7 and not turn.robber_moved:
                response = {"detail": "you have to move the thief"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            response = change_turn(game)
            # Solo tirar los dados si estoy en el juego...
            if game_stage == 'FULL_PLAY':
                throw_dices(game)
            return response
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
