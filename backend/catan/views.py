from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Card, Player
from .serializers import CardSerializer, PlayerSerializer


class CardsList(APIView):
    def get(self, request, pk):
        user = self.request.user
        user_id = User.objects.filter(username=user).get().id
        queryset = Card.objects.filter(player__username=user_id)
        serializer = CardSerializer(queryset, many=True)
        return Response(serializer.data)
