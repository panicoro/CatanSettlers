from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Card, Player, Resource, Game
from .serializers import CardSerializer, ResourceSerializer
from django.shortcuts import get_object_or_404


class PlayerInfo(APIView):
    def get(self, request, pk):
        game = get_object_or_404(Game, pk=pk)
        user = self.request.user
        player_id = Player.objects.filter(username=user, game=pk).get().id
        queryset_cards = Card.objects.filter(owner=player_id)
        queryset_resource = Resource.objects.filter(owner=player_id)
        serializer_cards = CardSerializer(queryset_cards, many=True)
        serializer_resource = ResourceSerializer(queryset_resource, many=True)
        data = {'resources': serializer_resource.data,
                'cards': serializer_cards.data}
        return Response(data)
