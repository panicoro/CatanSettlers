from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from catan.models import *
from catan.serializers import *
from django.http import Http404
from django.shortcuts import get_object_or_404


class PlayerInfo(APIView):
    def get(self, request, pk):
        resource_list = []
        game = get_object_or_404(Game, pk=pk)
        user = self.request.user
        player_id = Player.objects.filter(username=user, game=pk).get().id
        queryset_cards = Card.objects.filter(owner=player_id)
        queryset_resource = Resource.objects.filter(owner=player_id)
        serializer_cards = CardSerializer(queryset_cards, many=True)
        serializer_resource = ResourceSerializer(queryset_resource, many=True)
        for resource in serializer_resource.data:
            print(resource.values())
            resource_list.append(resource.values())
            print(resource_list)

        data = {'resources': resource_list,
                'cards': serializer_cards.data}
        return Response(data)
