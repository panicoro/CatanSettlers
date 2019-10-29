from catan.models import *
from random import random
from catan.cargaJson import HexagonInfo

class MoveRobber(APIView):
    def post(self, request, pk):
        data = request.data
        game = get_object_or_404(Game, pk=pk)
        user = self.request.user
        owner = Player.objects.filter(username=user, game=pk).get()
        level1 = int(data['payload']['level1'])
        index1 = int(data['payload']['index1'])
        # Verifica cuales son los jugadores que tienen ciudades o poblados
        # si hay mas de uno elige uno al azar