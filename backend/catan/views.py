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
