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

    def checkVertex(self, level, index):
        rta = False
        vertex = VertexPosition.objects.filter(level=level, index=index)
        if vertex.exists():
            rta = True
            return rta
        return rta

    def ResourceBuild(self, player_id, game_id):
        """
        Return a variable variable size list
        if you find the items.
        """
        list_resource = Resource.objects.filter(owner=player_id, game=game_id)
        brick = True
        lumber = True
        wool = True
        grain = True
        rta = []
        for resource in list_resource:
            if resource.resource_name == "brick" and brick:
                brick = False
                rta.append(resource)
            if resource.resource_name == "lumber" and lumber:
                lumber = False
                rta.append(resource)
            if resource.resource_name == "wool" and wool:
                wool = False
                rta.append(resource)
            if resource.resource_name == "grain" and grain:
                grain = False
                rta.append(resource)
        return rta

    def CheckPosition(self, game_id, level, index):
        rta = True
        position = VertexPosition.objects.filter(level=level,
                                                 index=index).get()
        building = Building.objects.filter(game=game_id, position=position)
        if building.exists():
            rta = False
            return rta
        return rta

    def CheckRoad(self, player_id, game_id, level, index):
        """
        Returns True if there is one of the vertices of the player's paths
        matches the VertexPosition entered by it.
        """
        vertex = VertexPosition.objects.filter(level=level, index=index).get()
        rta = False
        road_player = Road.objects.filter(Q(owner=player_id, game=game_id,
                                          vertex_1=vertex) |
                                          Q(owner=player_id, game=game_id,
                                          vertex_2=vertex))
        if road_player.exists():
            rta = True
        return rta

    def CheckBuild(self, game_id, level, index):
        """
        Returns True if there is no construction in the neighbors of the
        VertexPosition entered by the player.
        """
        list_build = Building.objects.filter(game=game_id)
        list_vertex = VertexInfo(level, index)
        rta = True
        for build in list_build:
            for vertex in list_vertex:
                if build.position.level == vertex[0]:
                    if build.position.index == vertex[1]:
                        rta = False
                        return rta
        return rta

    def deleteResource(self, list_resource):
        """
        Remove resources from the list.
        """
        for resource in list_resource:
            resource.delete()

    def Building(self, game, player, level, index):
        position = VertexPosition.objects.filter(level=level,
                                                 index=index).get()
        new_build = Building(game=game, name='settlement', owner=player,
                             position=position)
        new_build.save()
        point = player.victory_points + 1
        player.victory_points = point
        player.save()

    def Road(self, game, player, level1, index1, level2, index2):
        position_1 = VertexPosition.objects.filter(level=level1,
                                                   index=index1).get()
        position_2 = VertexPosition.objects.filter(level=level2,
                                                   index=index2).get()
        new_road = Road(game=game, vertex_1=position_1,
                        vertex_2=position_2, owner=player)
        new_road.save()

    def post(self, request, pk):
        data = request.data
        game = get_object_or_404(Game, pk=pk)
        player = get_object_or_404(Player, username=request.user, game=game)
        # Check if the player is on his turn
        if not self.check_player_in_turn(game, player):
            response = {"detail": "Not in turn"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        if data['type'] == 'build_settlement':
            level = data['payload']['level']
            index = data['payload']['index']
            # Check that the position exists
            if not self.checkVertex(level, index):
                response = {"detail": "Non-existent position"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            # Check that the position is available
            if not self.CheckPosition(game.id, level, index):
                response = {"detail": "Busy position"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            necessary_resources = self.ResourceBuild(player.id, game.id)
            # Check that the pleyer has the necessary resources
            if len(necessary_resources) != 4:
                response = {"detail": "It does not have" +
                            "the necessary resources"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            is_road = self.CheckRoad(player.id, game.id, level, index)
            is_building = self.CheckBuild(game.id, level, index)
            # Check that there are no building in the neighboring vertex
            # Checking that the player has a road in the vertex
            if not is_building or not is_road:
                response = {"detail": "Invalid position"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            self.Building(game, player, level, index)
            self.deleteResource(necessary_resources)
            return Response(status=status.HTTP_200_OK)

        user = self.request.user
        owner = Player.objects.filter(username=user, game=pk).get()
        # Check if the player is on his turn
        if not check_player_in_turn(game, owner):
            response = {"detail": "Not in turn"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        if data['type'] == 'build_road':
            level1 = data['payload'][0]['level']
            index1 = data['payload'][0]['index']
            level2 = data['payload'][1]['level']
            index2 = data['payload'][1]['index']
            # Check that the position exists
            if not checkVertexsPositions(level1, index1, level2, index2):
                response = {"detail": "Non-existent vetertexs positions"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            list_neighbor = VertexInfo(level1, index1)
            # check that the neighbor exists
            if not is_neighbor(list_neighbor, level2, index2):
                response = {"detail": "not neighbor"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            position_road = CheckPositionRoad(game.id, level1, index1,
                                              level2, index2)
            # I check if the position is free
            if position_road:
                response = {"detail": "invalid position, reserved"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            list_resources = ResourcesRoad(owner.id, game.id)
            # I verify necessary resources
            if len(list_resources) != 2:
                response = {"detail": "Doesn't have enough resources"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            is_roads = CheckRoads_Road(owner.id, game.id, level1, index1,
                                       level2, index2)
            is_building = CheckBuild_Road(owner.id, game.id, level1, index1,
                                          level2, index2)
            # I verify that I have my own road or building
            if not is_roads and not is_building:
                response = {"detail": "must have something built"}
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            self.Road(game, owner, level1, index1, level2, index2)
            deleteResource(owner.id, game.id)
            return Response(status=status.HTTP_200_OK)

