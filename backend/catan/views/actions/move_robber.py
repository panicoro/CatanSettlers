from catan.models import *
from rest_framework.response import Response
from rest_framework import status

HEXE_POSITIONS = generateHexesPositions()


def check_position(level, index):
    return [level, index] in HEXE_POSITIONS


def move_robber(payload, game, user, player, knight=False):
    if knight:
        if not player.has_card('knight'):
            response = {"detail": 'You have not knight cards'}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
    else:
        if game.get_sum_dices() != 7:
            response = {"detail": 'The sum dices is not 7'}
            return Response(response, status=status.HTTP_403_FORBIDDEN)
    level = payload['position']['level']
    index = payload['position']['index']
    choosen_player = payload['player']
    # Check if it is a valid position
    if not check_position(level, index):
        response = {"detail": "There is no hexe in that position"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    if not game.is_new_robber_position(level, index):
        response = {"detail": "You must enter a new hexe position"}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
    # Check if I want to steal myselft
    if choosen_player == user.username:
        response = {"detail": "You can't choose yourself"}
        return Response(response, status.HTTP_403_FORBIDDEN)
    players_to_steal = player.get_players_to_steal(level, index)
    if choosen_player not in players_to_steal and players_to_steal != []:
        response = {"detail": "You have to choose a player that has buildings"}
        return Response(response, status.HTTP_403_FORBIDDEN)
    if players_to_steal == []:
        game.move_robber(level, index)
        if knight:
            player.use_card('knight')
        return Response(status=status.HTTP_204_NO_CONTENT)
    else:
        game.move_robber(level, index)
        player.steal_to(choosen_player)
        if knight:
            player.use_card('knight')
        return Response(status=status.HTTP_204_NO_CONTENT)
