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
from catan.dices import throw_dices, gain_resources_free
from rest_framework.permissions import AllowAny
from random import shuffle
from django.db.models import Q
from aux.generateBoard import generateVertexPositions

VERTEX_POSITIONS = generateVertexPositions()


def exists_vertex(level, index):
    return [level, index] in VERTEX_POSITIONS


def can_build_settlement(player):
    """
    Return a variable variable size list
    if you find the items.
    """
    needed_resources = ['brick', 'lumber', 'wool', 'grain']
    for resource in needed_resources:
        resource_exists  = Resource.objects.filter(owner=player, 
                                                   name=resource).exists()
        if (not resource_exists):
            return False
    return True


def exists_building(game, level, index):
    """
    Return true is there's a bulding in the 
    vertex position with gaven level and index
    """
    return Building.objects.filter(game=game, level=level,
                                   index=index).exists()


def check_road(player_id, game_id, level, index):
    """
    Returns True if there is one of the vertices of the player's paths
        matches the VertexPosition entered by it.
    """
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
    """

def check_build(game_id, level, index):
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


def check_winner(game, player):
    winner = False
    points = player.victory_points
    card_vic_points = Card.objects.filter(
        game=game, owner=player,
        card_name='victory_point').count()
    suma_total = points + card_vic_points

    if suma_total == 10:
        winner = True
        user = User.objects.get(username=player.username)
        game.winner = user
        game.save()
    return winner


def delete_resources(player):
    """
    Remove resources from the list.
    """
    needed_resources = ['brick', 'lumber', 'wool', 'grain']
    for resource in needed_resources:
        Resource.objects.get(owner=player, name=resource).delete()


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

def to_json_positions(list_positions):
    data = []
    for position in list_positions:
        data.append({'level': position[0], 
                     'index': position[1]})
    return data

def posibles_initial_settlements(game):
    """
    A function that obtains positions that a player might have
    available to build settlements on the board during the
    construction stage
    """
    vertex_available = VERTEX_POSITIONS
    # Get all the buildings
    buildings = Building.objects.filter(game=game)
    if len(buildings) == 0:
        return to_json_positions(vertex_available)
    else:
        for building in buildings:
            building_vertex = [building.level, building.index]
            if building_vertex in vertex_available:
                vertex_available.remove(building_vertex)
            neighbors = VertexInfo(building.level, building.index)
            for neighbor in neighbors:
                if neighbor in vertex_available:
                    vertex_available.remove(neighbor)
        return to_json_positions(vertex_available)

def posiblesSettlements(player):
    """
    A function that obtains positions that a player might have
    available to build settlements on the board.
    Args:
    @player: a player of a started game.
    """
    (vertex_roads, vertex_buildings) = get_roadsAndBuildings(player)
    # I get the vertices of my own roads that are not occupied by my buildings
    available_vertex = vertex_roads - vertex_buildings
    # For each vertices check that their neighbors are not occupied,
    # if they are it can not be built (distance rule)
    potencial_buildings = list(available_vertex)
    for vertex in available_vertex:
        # Get the neighbors of a vertex position
        neighbors = VertexInfo(vertex.level, vertex.index)
        """
        for neighbor in neighbors:
            vertex_position = VertexPosition.objects.filter(
                                level=neighbor[0],
                                index=neighbor[1]).get()
            # If there a building in one of the neighbors then
            # the vertex couldn't have a new building...
            if Building.objects.filter(position=vertex_position).exists():
                potencial_buildings.remove(vertex)
                break
        """
    return potencial_buildings


def build_settlement(payload, game, player):
    level = payload['level']
    index = payload['index']
    # Check that the position exists
    if not exists_vertex(level, index):
        response = {"detail": "Non-existent position"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    # Check that the position is available
    if exists_building(game, level, index):
        response = {"detail": "Busy position"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    game_stage = game.current_turn.game_stage
    if game_stage == 'FULL_PLAY':
        # Check that the pleyer has the necessary resources if he not in the
        if not can_build_settlement(player):
            response = {"detail": "It does not have" +
                        "the necessary resources"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        is_road = check_road(player.id, game.id, level, index)
        is_building = check_build(game.id, level, index)
        # Check that there are no building in the neighboring vertex
        # Checking that the player has a road in the vertex
        if not is_building or not is_road:
            response = {"detail": "Invalid position"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        delete_resources(player)
    new_build = Building(game=game, name='settlement', owner=player,
                         level=level, index=index)
    new_build.save()
    game.current_turn.last_action = 'BUILD_SETTLEMENT'
    game.current_turn.save()
    #if game_stage == 'SECOND_CONSTRUCTION':
    #    gain_resources_free(game, player, position)
    # Add a new method in player
    point = player.victory_points + 1
    player.victory_points = point
    player.save()
    # Check if the player won
    if check_winner(game, player):
        response = {"detail": "YOU WIN!!!"}
        return Response(response, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_200_OK)
