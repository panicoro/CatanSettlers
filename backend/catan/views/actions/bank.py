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


# Look for the resources you want to give.
def resource_search(game, player, give):
    list_resource = Resource.objects.filter(owner=player, game=game,
                                            resource_name=give)
    return list_resource


# delete the resource you want to give.
def deleteResource(owner_id, game_id, give):
    list_resource = Resource.objects.filter(owner=owner_id, game=game_id,
                                            resource_name=give)
    for resource in list_resource:
        resource.delete()


# update player resource amount
def update_rec_player(player, game, receive):
    new_resource = Resource.objects.create(owner=player, game=game,
                                           resource_name=receive)
    new_resource.save()


# bank trade view
def bank_trade(payload, game, player):
    give = payload['give']
    receive = payload['receive']
    new_list_rec = resource_search(game, player, give)
    if len(new_list_rec) < 4:
        response = {'No tiene la cantidad de recursos suficientes'}
        return Response(data=response, status=status.HTTP_403_FORBIDDEN)
    deleteResource(player, game, give)
    update_rec_player(player, game, receive)
    return Response(status=status.HTTP_200_OK)
