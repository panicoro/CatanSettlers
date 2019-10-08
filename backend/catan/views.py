from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Game, Resource
from .serializers import GameSerializer,    ResourceSerializer
from django.http import Http404

class ResourceList(APIView):

    def get_object(self, request):
        print(request.user)
        print("Hola")
        queryset = Resource.objects.all()
        serializer = ResourceSerializer(queryset)
        return Response(serializer.data)