from catan.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt import authentication
from django.http import Http404
from random import random
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from aux.json_load import *
from rest_framework.permissions import AllowAny
from random import shuffle
from django.db.models import Q


VERTEX_POSITIONS = generateVertexPositions()


def are_neighbors(level_1, index_1, level_2, index_2):
    """
    Check if the vertexs are neighbors.
    """
    list_neighbor = VertexInfo(level_1, index_1)
    return [level_2, index_2] in list_neighbor


def check_range_vertex_positions(level1, index1, level2, index2):
    """
    Check that the vertices exist within the allowed range
    """
    vertex_1 = [level1, index1] in VERTEX_POSITIONS
    vertex_2 = [level2, index2] in VERTEX_POSITIONS
    return vertex_1 and vertex_2


def build_road(payload, game, player, road_building_card=False):
    level_1 = payload[0]['level']
    index_1 = payload[0]['index']
    level_2 = payload[1]['level']
    index_2 = payload[1]['index']
    game_stage = game.current_turn.game_stage
    # Check that the position is valid
    if not check_range_vertex_positions(level_1, index_1, level_2, index_2):
        response = {"detail": "Non-existent vertexs positions"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    # check that the vertex are neighbors
    list_neighbor = VertexInfo(level_1, index_1)
    if not are_neighbors(level_1, index_1, level_2, index_2):
        response = {"detail": "not neighbors"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    # I check if the position is free
    if game.exists_road(level_1, index_1, level_2, index_2):
        response = {"detail": "Busy position, reserved"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    if game_stage == 'FULL_PLAY':
        # I verify that I have my own road or building
        if not player.check_roads_continuation(level_1, index_1,
                                               level_2, index_2):
            response = {"detail": "You must have something built"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
    else:
        last_building = Building.objects.filter(owner=player).last()
        last_level_1 = last_building.level
        last_index_1 = last_building.index
        # I verify that I have my last building
        if not player.check_roads_continuation(last_level_1, last_index_1,
                                               level_2, index_2,
                                               only_building=True):
            response = {"detail": "must built since your last building"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
    if (road_building_card is False) and (game_stage == 'FULL_PLAY'):
        # I verify necessary resources
        # cambiar por la funcon del player idem con delete
        if not player.has_necessary_resources('build_road'):
            response = {"detail": "Doesn't have enough resources"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        player.delete_resources('build_road')
    # sacar funcion de create es al pedo
    Road.objects.create(game=game, owner=player,
                        level_1=level_1, index_1=index_1,
                        level_2=level_2, index_2=index_2)
    game.current_turn.last_action = 'BUILD_ROAD'
    game.current_turn.save()
    return Response(status=status.HTTP_200_OK)


def play_road_building_card(payload, game, player):
    cards = Card.objects.filter(game=game,
                                owner=player,
                                name="road_building")
    if not player.has_card('road_building'):
        response = {"detail": "Missing Road Building card"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    position_1 = payload[0]
    position_2 = payload[1]
    level_1 = position_1[0]['level']
    index_1 = position_1[0]['index']
    level_2 = position_1[1]['level']
    index_2 = position_1[1]['index']
    payload_2 = [{"level": level_1, "index": index_1},
                 {"level": level_2, "index": index_2}]
    br = build_road(payload_2, game, player, road_building_card=True)
    if "403" in str(br):
        return br
    level_3 = position_2[0]['level']
    index_3 = position_2[0]['index']
    level_4 = position_2[1]['level']
    index_4 = position_2[1]['index']
    payload2 = [{"level": level_3, "index": index_3},
                {"level": level_4, "index": index_4}]
    br = build_road(payload2, game, player, road_building_card=True)
    if "403" in str(br):
        Road.objects.filter(owner=player.id,
                            level_1=level_1, level_2=level_2,
                            index_1=index_1, index_2=index_2,
                            game=game)[0].delete()
        return br
    player.use_card('road_building')
    return Response(status=status.HTTP_200_OK)
