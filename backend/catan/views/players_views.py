from rest_framework.views import APIView
from django.contrib.auth.models import User
from catan.serializers import *
from django.http import Http404
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from catan.models import *
from rest_framework.permissions import AllowAny
from random import shuffle
from catan.views.actions.road import build_road, play_road_building_card
from catan.views.actions.buy_card import buy_card
from catan.views.actions.bank import bank_trade
from catan.views.actions.build import build_settlement
from catan.views.actions.move_robber import move_robber
from catan.views.actions.change_turn import change_turn


class PlayerInfo(APIView):
    def get(self, request, pk):
        resource_list = []
        card_list = []
        game = get_object_or_404(Game, pk=pk)
        user = self.request.user
        player = Player.objects.filter(username=user, game=pk).get().id
        queryset_card = Card.objects.filter(Q(owner=player) &
                                            (Q(name='knight') |
                                            Q(name='monopoly') |
                                            Q(name='year_of_plenty') |
                                            Q(name='road_building') |
                                            Q(name='victory_point')))
        queryset_resource = Resource.objects.filter(Q(owner=player) &
                                                    (Q(name='ore') |
                                                     Q(name='brick') |
                                                     Q(name='lumber') |
                                                     Q(name='grain') |
                                                     Q(name='wool')))
        serializer_card = CardSerializer(queryset_card, many=True)
        serializer_resource = ResourceSerializer(queryset_resource, many=True)
        for resource in serializer_resource.data:
            resource_list.append(resource['name'])
        for card in serializer_card.data:
            card_list.append(card['name'])
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
            item['payload'].append(self.to_json_positions(road))
        return item

    def posible_robber_positions(self, game):
        """
        A function that obtains the possible positions
        where the thief can move and for each of them, the players to steal.
        """
        hexes_positions_robber = generateHexesPositions()
        actual_robber = [game.robber.level, game.robber.index]
        hexes_positions_robber.remove(actual_robber)
        data = []
        for hexe in hexes_positions_robber:
            item = {'position': {
                                    'level': hexe[0],
                                    'index': hexe[1]
                                }
                    }
            neighbors = HexagonInfo(hexe[0], hexe[1])
            item['players'] = []
            for neighbor in neighbors:
                try:
                    building = Building.objects.get(level=neighbor[0],
                                                    index=neighbor[1],
                                                    game=game)
                    new_user = building.owner.username.username
                    if new_user not in item['players'] and \
                            new_user != game.current_turn.user.username:
                        item['players'].append(new_user)
                except Building.DoesNotExist:
                    pass
            data.append(item)
        return data

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
                posibles_settlements = game.posibles_initial_settlements()
                item['payload'] = self.to_json_positions(posibles_settlements)
                data.append(item)
            if last_action == 'BUILD_SETTLEMENT':
                item = {"type": 'build_road'}
                posibles_roads = player.posibles_initial_roads()
                item['payload'] = []
                for road in posibles_roads:
                    item['payload'].append(self.to_json_positions(road))
                data.append(item)
            if last_action == 'BUILD_ROAD':
                item = {"type": 'end_turn'}
                data.append(item)
            return Response(data, status=status.HTTP_200_OK)
        else:
            if game.get_sum_dices() == 7 and not game.robber_has_been_moved():
                item = {"type": 'move_robber'}
                posibles_robber = self.posible_robber_positions(game)
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
                if player.can_trade_bank():
                    item = {"type": 'bank_trade'}
                    data.append(item)
                if player.has_necessary_resources('buy_card'):
                    item = {"type": 'buy_card'}
                    data.append(item)
                if player.has_necessary_resources('build_settlement'):
                    item = {"type": 'build_settlement'}
                    posibles_settlements = player.posibles_settlements()
                    item['payload'] = self.to_json_positions(
                                        posibles_settlements)
                    if len(item['payload']) != 0:
                        data.append(item)
                if player.has_card('knight'):
                    item = {"type": 'play_knight_card'}
                    posibles_robber = self.posible_robber_positions(game)
                    item["payload"] = posibles_robber
                    data.append(item)
                if player.has_card('road_building'):
                    item = {"type": 'play_road_building_card'}
                    posibles_roads = player.posibles_roads_card_road_building()
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
            if game.get_sum_dices() == 7 and not game.robber_has_been_moved():
                response = {"detail": "You have to move the thief"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            response = change_turn(game)
            # Only throw the dices if I am in full play...
            if game_stage == 'FULL_PLAY':
                game.throw_dices()
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
            response = move_robber(data['payload'], game,
                                   user, player)
            return response
        if data['type'] == 'play_knight_card':
            response = move_robber(data['payload'], game,
                                   user, player, knight=True)
            return response
        if data['type'] == 'play_road_building_card':
            response = play_road_building_card(data['payload'], game, player)
            return response
        response = {"detail": 'Please select a valid action'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
