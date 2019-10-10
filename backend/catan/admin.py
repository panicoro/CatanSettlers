from django.contrib import admin
from catan.models import Card, Player, Vertex_position_settlements
from catan.models import Vertex_position_cities, Road_position, Last_gained, Resource

admin.site.register(Card)
admin.site.register(Player)
admin.site.register(Vertex_position_settlements)
admin.site.register(Vertex_position_cities)
admin.site.register(Road_position)
admin.site.register(Last_gained)
admin.site.register(Resource)
