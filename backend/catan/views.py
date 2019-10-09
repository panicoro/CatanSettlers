from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Game, Resource, Player
from .serializers import GameSerializer, ResourceSerializer, PlayerSerializer
from django.http import Http404

class ResourceList(APIView):

    def get(self, request, pk):        
        user = self.request.user
        player_id = Player.objects.filter(username=user).get().id
        queryset = Resource.objects.filter(owner=player_id)
        serializer = ResourceSerializer(queryset, many=True)
        return Response(serializer.data)