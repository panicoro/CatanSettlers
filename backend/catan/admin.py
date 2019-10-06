from django.contrib import admin
from .models import *

class TableroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')

class HexagonoAdmin(admin.ModelAdmin):
    list_display = ('resource', 'token', 'tablero')

class VerticeAdmin(admin.ModelAdmin):
    list_display = ('nivel', 'indice', 'tablero')

admin.site.register(Tablero, TableroAdmin)
admin.site.register(Hexagono, HexagonoAdmin)
admin.site.register(Vertice, VerticeAdmin)