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
from catan.dices import throw_dices
from rest_framework.permissions import AllowAny
from random import shuffle
from django.db.models import Q


# get the necessary resources
def ResourcesRoad(owner_id, game_id):
    list_resource = Resource.objects.filter(owner=owner_id, game=game_id)
    brick = True
    lumber = True
    rta = []

    for resource in list_resource:
        if resource.resource_name == "brick" and brick:
            rta.append(resource)
            brick = False
        if resource.resource_name == "lumber" and lumber:
            rta.append(resource)
            lumber = False
    return rta


def canBuild_Road(player):
    resources = ResourcesRoad(player, player.game)
    return len(resources) == 2


# check the existence of a built road
def CheckRoads_Road(owner_id, game_id, level1, index1, level2, index2):
    list_road = Road.objects.filter(owner=owner_id, game=game_id)
    rta = False
    for road in list_road:
        if road.vertex_1.level == level1:
            if road.vertex_1.index == index1:
                rta = True
                return rta
        if road.vertex_2.level == level1:
            if road.vertex_2.index == index1:
                rta = True
                return rta
        if road.vertex_1.level == level2:
            if road.vertex_1.index == index2:
                rta = True
                return rta
        if road.vertex_2.level == level2:
            if road.vertex_2.index == index2:
                rta = True
                return rta
    return rta


# check the existence of a built building
def CheckBuild_Road(owner_id, game_id, level1, index1, level2, index2):
    list_build = Building.objects.filter(owner=owner_id, game=game_id)
    rta = False
    for build in list_build:
        if build.position.level == level1:
            if build.position.index == index1:
                rta = True
                return rta
        if build.position.level == level2:
            if build.position.index == index2:
                rta = True
                return rta
    return rta


# check if the position given for the new road is repeated
def CheckPositionRoad(game_id, level1, index1, level2, index2):
    list_all_road = Road.objects.filter(game=game_id)
    rta = False
    for road in list_all_road:
        if road.vertex_1.level == level1:
            if road.vertex_1.index == index1:
                if road.vertex_2.level == level2:
                    if road.vertex_2.index == index2:
                        rta = True
                        return rta
        if road.vertex_1.level == level2:
            if road.vertex_1.index == index2:
                if road.vertex_2.level == level1:
                    if road.vertex_2.index == index1:
                        rta = True
                        return rta
    return rta


# delete resource
def deleteResource(owner_id, game_id):
    list_resource = Resource.objects.filter(owner=owner_id, game=game_id)
    for resource in list_resource:
        resource.delete()


# check if it's neighbor
def is_neighbor(list_neighbor, level, index):
    vec = False
    for v in list_neighbor:
        if v[0] == level and v[1] == index:
            vec = True
            return vec
    return vec


# check that the vertices exist within the allowed range
def checkVertexsPositions(level1, index1, level2, index2):
    exist_v = False
    position_1 = VertexPosition.objects.filter(level=level1,
                                               index=index1)
    position_2 = VertexPosition.objects.filter(level=level2,
                                               index=index2)
    if position_1.exists() and position_2.exists():
        exist_v = True
        return exist_v
    return exist_v


def create_Road(game, player, level1, index1, level2, index2):
    position_1 = VertexPosition.objects.filter(level=level1,
                                               index=index1).get()
    position_2 = VertexPosition.objects.filter(level=level2,
                                               index=index2).get()
    new_road = Road(game=game, vertex_1=position_1,
                    vertex_2=position_2, owner=player)
    new_road.save()


def get_roadsAndBuildings(player):
    """
    A function that obtains two set of vertex positions of
    the roads and buildings of a given player.
    Args:
    @player: a player of a started game.

    """
    roads = Road.objects.filter(owner=player)
    vertex_roads = set()
    for road in roads:
        vertex_roads.add(road.vertex_1)
        vertex_roads.add(road.vertex_2)
    buildings = Building.objects.filter(owner=player)
    vertex_buildings = set()
    for build in buildings:
        vertex_buildings.add(build.position)
    return (vertex_roads, vertex_buildings)


def get_potencialRoads(available_vertex):
    """
    A function that receives a list of available vertices and
    returns a list of positions (ROAD_POSITIONS) in which roads
    can be constructed from the vertices given in the list
    Args:
    @avalaible_vertex: a list of vertex positions (objects)
    """
    potencial_roads = []
    for vertex in available_vertex:
        # Get the neighbors of a vertex
        neighbors = VertexInfo(vertex.level, vertex.index)
        for neighbor in neighbors:
            vertex_position = VertexPosition.objects.filter(
                                level=neighbor[0],
                                index=neighbor[1]).get()
            if not Road.objects.filter(Q(vertex_1=vertex,
                                       vertex_2=vertex_position) |
                                       Q(vertex_1=vertex_position,
                                       vertex_2=vertex)).exists():
                new_road = [vertex, vertex_position]
                potencial_roads.append(new_road)
    return potencial_roads


def posiblesRoads(player):
    """
    A function that obtains positions that a player might have
    available to build roads on the board.
    Args:
    @player: a player of a started game.
    """
    (vertex_roads, vertex_buildings) = get_roadsAndBuildings(player)
    available_vertex = vertex_buildings.union(vertex_roads)
    potencial_roads = get_potencialRoads(available_vertex)
    return potencial_roads


def posiblesRoads_cardRoadBuilding(player):
    """
    A function that obtains posistions that a player might have
    available to build the two roads using the Card road_building
    Args:
    @player: a player of a started game.
    """
    potencial_roads = posiblesRoads(player)
    new_positions = []
    for road in potencial_roads:
        new_positions.append(road[1])
    new_potencial_roads = get_potencialRoads(new_positions)
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
    level1 = payload[0]['level']
    index1 = payload[0]['index']
    level2 = payload[1]['level']
    index2 = payload[1]['index']
    # Check that the position exists
    if not checkVertexsPositions(level1, index1, level2, index2):
        response = {"detail": "Non-existent vetertexs positions"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    if road_building_card is False:
        list_resources = ResourcesRoad(owner.id, game.id)
        # I verify necessary resources
        if len(list_resources) != 2:
            response = {"detail": "Doesn't have enough resources"}
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
    is_roads = CheckRoads_Road(owner.id, game.id, level1, index1,
                               level2, index2)
    is_building = CheckBuild_Road(owner.id, game.id, level1, index1,
                                  level2, index2)
    # I verify that I have my own road or building
    if not is_roads and not is_building:
        response = {"detail": "must have something built"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    create_Road(game, owner, level1, index1, level2, index2)
    if road_building_card is False:
        deleteResource(owner.id, game.id)
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
    level1 = position_1[0]['level']
    index1 = position_1[0]['index']
    level2 = position_1[1]['level']
    index2 = position_1[1]['index']
    payload2 = [{"level": level1, "index": index1},
                {"level": level2, "index": index2}]
    br = build_road(payload2, game, player, road_building_card=True)
    if "403" in str(br):
        return br
    level3 = position_2[0]['level']
    index3 = position_2[0]['index']
    level4 = position_2[1]['level']
    index4 = position_2[1]['index']
    payload2 = [{"level": level3, "index": index3},
                {"level": level4, "index": index4}]
    br = build_road(payload2, game, player, road_building_card=True)
    if "403" in str(br):
        vertex1 = VertexPosition.objects.filter(level=level1, index=index1)
        vertex2 = VertexPosition.objects.filter(level=level2, index=index2)
        Road.objects.filter(owner=player.id,
                            vertex_1=vertex1[0],
                            vertex_2=vertex2[0],
                            game=game.id)[0].delete()
        return br
    deleteCard(game.id, player.id)
    cards = Card.objects.filter(game=game, owner=player)
    return Response(status=status.HTTP_200_OK)
