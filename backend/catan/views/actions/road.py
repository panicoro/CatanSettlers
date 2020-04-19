from catan.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt import authentication
from django.http import Http404
from random import random
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from catan.cargaJson import *
from aux.generateBoard import generateVertexPositions
from catan.dices import throw_dices
from rest_framework.permissions import AllowAny
from random import shuffle
from catan.views.actions.build import delete_resources
from django.db.models import Q
from catan.views.actions.build import to_json_positions


VERTEX_POSITIONS = generateVertexPositions()


def can_build_road(player):
    """
    Return a variable variable size list
    if you find the items.
    """
    needed_resources = ['brick', 'lumber']
    for resource in needed_resources:
        resource_exists  = Resource.objects.filter(owner=player, 
                                                   name=resource).exists()
        if (not resource_exists):
            return False
    return True

def delete_resources(player):
    """
    Remove resources from the list.
    """
    needed_resources = ['brick', 'lumber']
    for resource in needed_resources:
        Resource.objects.get(owner=player, name=resource).delete()

def check_roads_road(owner, game, level1, index1, level2, index2):
    """

    """
    road_1 = Road.objets.filter(owner=owner, game=game,
                       level_1=level1, index_1=index1,
                       level_2=level2, index_2=index2).exists()
    road_2 = Road.objets.filter(owner=owner, game=game,
                       level_1=level2, index_1=index2,
                       level_2=level1, index_2=index1).exists()
    return road_1 or road_2


def check_build_road(owner, game, level1, index1, level2, index2):
    """
    """
    building_1 = Building.objects.filter(owner=owner, game=game,
                                        level=level1,
                                        index=index1).exists()
    building_2 = Building.objects.filter(owner=owner, game=game,
                                        level=level2,
                                        index=index2).exists()
    return building_1 or building_2    
    

# check if the position given for the new road is repeated
def check_position_road(game, level1, index1, level2, index2):
    """
    """
    road_1 = Road.objects.filter(game=game,
                                level_1=level1, index_1=index1,
                                level_2=level2, index_2=index2).exists()
    road_2 = Road.objects.filter(game=game,
                                level_1=level2, index_1=index2,
                                level_2=level1, index_2=index1).exists()
    return road_1 or road_2


# check if it's neighbor
def is_neighbor(list_neighbor, level, index):
    vec = False
    for v in list_neighbor:
        if v[0] == level and v[1] == index:
            vec = True
            return vec
    return vec


# check that the vertices exist within the allowed range
def check_vertex_positions(level1, index1, level2, index2):
    vertex_1 = [level1, index1] in VERTEX_POSITIONS
    vertex_2 = [level2, index2] in VERTEX_POSITIONS
    return vertex_1 and vertex_2
    

def create_road(game, player, level1, index1, level2, index2):
    new_road = Road(game=game, level_1=level1, level_2=level2,
                    index_1=index1, index_2=index2, owner=player)
    new_road.save()


def get_roads_and_buildings(player):
    """
    A function that obtains two set of vertex positions of
    the roads and buildings of a given player.
    Args:
    @player: a player of a started game.
    """
    roads = Road.objects.filter(owner=player)
    vertex_roads = set()
    for road in roads:
        vertex_1 = [road.level_1, road.index_1]
        vertex_2 = [road.level_2, road.index_2]
        vertex_roads.add(vertex_1)
        vertex_roads.add(vertex_2)
    buildings = Building.objects.filter(owner=player)
    vertex_buildings = set()
    for build in buildings:
        vertex = [build.level, build.index]
        vertex_buildings.add(vertex)
    return (vertex_roads, vertex_buildings)

def to_json(vertex):
    return {'level': vertex[0], 'index': vertex[1]}

def posibles_initial_roads(player):
    building = Building.objects.filter(owner=player).last()
    potencial_roads = []
    vertex = [building.level, building.index]
    neighbors = VertexInfo(vertex[0], vertex[1])
    for neighbor in neighbors:
        new_road = [to_json(vertex),
                    to_json(neighbor)]
        potencial_roads.append(new_road)
    return potencial_roads


def get_potencial_roads(available_vertex):
    """
    A function that receives a list of available vertices and
    returns a list of positions (ROAD_POSITIONS) in which roads
    can be constructed from the vertices given in the list
    Args:
    @avalaible_vertex: a list of vertex positions ([level, index])
    """
    potencial_roads = []
    for vertex in available_vertex:
        # Get the neighbors of a vertex
        neighbors = VertexInfo(vertex[0], vertex[1])
        for neighbor in neighbors:
            if not Road.objects.filter(Q(level_1=vertex[0],
                                       index_1= vertex[1],
                                       level_2=neighbor[0],
                                       index_2=neighbor[1]) |
                                       Q(level_1=neighbor[0],
                                       index_1 =neighbor[1],
                                       level_2=vertex[0],
                                       index_2=vertex[1])).exists():
                new_road = [vertex, neighbor]
                potencial_roads.append(new_road)
    return potencial_roads


def posibles_roads(player):
    """
    A function that obtains positions that a player might have
    available to build roads on the board.
    Args:
    @player: a player of a started game.
    """
    (vertex_roads, vertex_buildings) = get_roads_and_buildings(player)
    available_vertex = vertex_buildings.union(vertex_roads)
    potencial_roads = get_potencial_roads(available_vertex)
    return potencial_roads


def posibles_roads_card_road_building(player):
    """
    A function that obtains posistions that a player might have
    available to build the two roads using the Card road_building
    Args:
    @player: a player of a started game.
    """
    potencial_roads = posibles_roads(player)
    new_positions = []
    for road in potencial_roads:
        new_positions.append(road[1])
    new_potencial_roads = get_potencial_roads(new_positions)
    total_roads = potencial_roads + new_potencial_roads
    # Remove the repeat road
    final_roads = total_roads
    for road in total_roads:
        invert_road = [road[1], road[0]]
        if invert_road in final_roads:
            final_roads.remove(invert_road)
    return final_roads


def deleteCard(game_id, player_id):
    # Corregir para que solo borre una carta
    # Esta borrando todas las cartas...
    card = Card.objects.filter(owner=player_id, game=game_id,
                               card_name='road_building')[0]
    card.delete()


def build_road(payload, game, owner, road_building_card=False):
    level_1 = payload[0]['level']
    index_1 = payload[0]['index']
    level_2 = payload[1]['level']
    index_2 = payload[1]['index']
    game_stage = game.current_turn.game_stage
    # Check that the position exists
    if not check_vertex_positions(level_1, index_1, level_2, index_2):
        response = {"detail": "Non-existent vetertexs positions"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    position_road = check_position_road(game, level_1, index_1,
                                        level_2, index_2)
    # I check if the position is free
    if position_road:
        response = {"detail": "invalid position, reserved"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    list_neighbor = VertexInfo(level_1, index_1)
    # check that the neighbor exists
    if not is_neighbor(list_neighbor, level_2, index_2):
        response = {"detail": "not neighbor"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    if game_stage == 'FULL_PLAY':
        is_roads = check_roads_road(owner, game, level_1, index_1,
                                   level_2, index_2)
        is_building = check_build_road(owner, game, level_1, index_1,
                                      level_2, index_2)
        # I verify that I have my own road or building
        if not is_roads and not is_building:
            response = {"detail": "must have something built"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
    else:
        last_building = Building.objects.filter(owner=owner).last()
        last_level_1 = last_building.level
        last_index_1 = last_building.index
        is_building = check_build_road(owner, game, last_level_1,
                                       last_index_1, level_2, index_2)
        # I verify that I have my last building
        if not is_building:
            response = {"detail": "must built since your last building"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
    if (road_building_card is False) and (game_stage == 'FULL_PLAY'):
        # I verify necessary resources
        if not can_build_road(owner):
            response = {"detail": "Doesn't have enough resources"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        delete_resources(owner)
    create_road(game, owner, level_1, index_1, level_2, index_2)
    game.current_turn.last_action = 'BUILD_ROAD'
    game.current_turn.save()
    return Response(status=status.HTTP_200_OK)


def play_road_building_card(payload, game, player):
    cards = Card.objects.filter(game=game,
                                owner=player,
                                card_name="road_building")
    if len(cards) == 0:
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
    deleteCard(game, player)
    return Response(status=status.HTTP_200_OK)
