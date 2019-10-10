from django.contrib import admin
from .models import *

class BoardAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

class HexesAdmin(admin.ModelAdmin):
    list_display = ('position', 'resource', 'token', 'board')

class VertexAdmin(admin.ModelAdmin):
    list_display = ('level', 'index', 'board')

class VertexPositionAdmin(admin.ModelAdmin):
    list_display = ('level', 'index')

class GameAdmin(admin.ModelAdmin):
    list_display = ('id','name','in_turn', 'board')

admin.site.register(Board, BoardAdmin)
admin.site.register(Hexes, HexesAdmin)
admin.site.register(Vertex, VertexAdmin)
admin.site.register(VertexPosition, VertexPositionAdmin)
admin.site.register(Game, GameAdmin)