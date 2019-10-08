from django.contrib import admin
from .models import *

class TableroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

class HexagonoAdmin(admin.ModelAdmin):
    list_display = ('position', 'resource', 'token', 'tablero')

class VerticeAdmin(admin.ModelAdmin):
    list_display = ('nivel', 'indice', 'tablero')

class VertexPositionAdmin(admin.ModelAdmin):
    list_display = ('level', 'index')

admin.site.register(Tablero, TableroAdmin)
admin.site.register(Hexagono, HexagonoAdmin)
admin.site.register(Vertice, VerticeAdmin)
admin.site.register(VertexPosition, VertexPositionAdmin)