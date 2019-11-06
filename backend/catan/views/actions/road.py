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


def checkCard(game_id, player_id):
    rta = False
    card = Card.objects.filter(owner=player_id, game=game_id,
                               card_name='road_building')[:1]
    if card.exists():
        rta = True
        return rta
    return rta


def deleteCard(game_id, player_id):
    card = Card.objects.filter(owner=player_id, game=game_id,
                               card_name='road_building')
    card.delete()


def build_road(payload, game, owner):
    level1 = payload[0]['level']
    index1 = payload[0]['index']
    level2 = payload[1]['level']
    index2 = payload[1]['index']
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
    create_Road(game, owner, level1, index1, level2, index2)
    deleteResource(owner.id, game.id)
    return Response(status=status.HTTP_200_OK)


def play_road_building_card(payload, game, player):
    position_1 = payload[0]
    position_2 = payload[1]
    level1 = position_1[0]['level']
    index1 = position_1[0]['index']
    level2 = position_1[1]['level']
    index2 = position_1[1]['index']
    level3 = position_2[0]['level']
    index3 = position_2[0]['index']
    level4 = position_2[1]['level']
    index4 = position_2[1]['index']
    # Check the player owns the card
    if not checkCard(game.id, player.id):
        response = {"detail": "Does not have the letter"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    # Check that the position exists
    if (not checkVertexsPositions(level1, index1, level2, index2) or
            not checkVertexsPositions(level3, index3, level4, index4)):
        response = {"detail": "Non-existent vetertexs positions"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    listNeighbor_road1 = VertexInfo(level1, index1)
    listNeighbor_road2 = VertexInfo(level3, index3)
    # check that the neighbor exists
    if (not is_neighbor(listNeighbor_road1, level2, index2) or
            not is_neighbor(listNeighbor_road2, level4, index4)):
        response = {"detail": "not neighbor"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    position_road1 = CheckPositionRoad(game.id, level1, index1,
                                       level2, index2)
    position_road2 = CheckPositionRoad(game.id, level3, index3,
                                       level3, index3)
    # I check if the position is free
    if position_road1 or position_road2:
        response = {"detail": "invalid position, reserved"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    isRoads_road1 = CheckRoads_Road(player.id, game.id, level1, index1,
                                    level2, index2)
    isBuilding_road1 = CheckBuild_Road(player.id, game.id, level1, index1,
                                       level2, index2)
    isRoads_road2 = CheckRoads_Road(player.id, game.id, level1, index1,
                                    level2, index2)
    isBuilding_road2 = CheckBuild_Road(player.id, game.id, level1, index1,
                                       level2, index2)
    # I verify that I have my own road or building
    if (not isRoads_road1 and not isBuilding_road1 and
            not isRoads_road2 and not isBuilding_road2):
        response = {"detail": "must have something built"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    create_Road(game, player, level1, index1, level2, index2)
    create_Road(game, player, level3, index3, level4, index4)
    deleteCard(game.id, player.id)
    return Response(status=status.HTTP_200_OK)
