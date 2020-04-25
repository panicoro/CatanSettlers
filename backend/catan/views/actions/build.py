from catan.models import *
from rest_framework.response import Response
from rest_framework import status

VERTEX_POSITIONS = generateVertexPositions()


def exists_vertex(level, index):
    return [level, index] in VERTEX_POSITIONS


def build_settlement(payload, game, player):
    level = payload['level']
    index = payload['index']
    # Check that the position exists
    if not exists_vertex(level, index):
        response = {"detail": "Non-existent position"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    # Check that the position is available
    if game.exists_building(level, index):
        print("fsdf")
        response = {"detail": "Busy position"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    game_stage = game.current_turn.game_stage
    if game_stage == 'FULL_PLAY':
        # Check that the pleyer has the necessary resources if he not in the
        if not player.has_necessary_resources('build_settlement'):
            response = {"detail": "It does not have" +
                        "the necessary resources"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        is_road = player.check_my_road(level, index)
        is_building = game.check_not_building(level, index)
        # Check that there are no building in the neighboring vertex
        # Checking that the player has a road in the vertex
        if not is_building or not is_road:
            response = {"detail": "Invalid position"}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        player.delete_resources('build_settlement')
    new_build = Building(game=game, name='settlement', owner=player,
                         level=level, index=index)
    new_build.save()
    game.current_turn.last_action = 'BUILD_SETTLEMENT'
    game.current_turn.save()
    # if game_stage == 'SECOND_CONSTRUCTION':
    #    gain_resources_free(game, player, position)
    # Add a new method in player
    player.gain_points(1)
    # Check if the player won
    if player.is_winner():
        response = {"detail": "YOU WIN!!!"}
        return Response(response, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_200_OK)
