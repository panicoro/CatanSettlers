from django.db import models


class Tablero(models.Model):
    nombre = models.CharField(max_length=25, blank=True, default='')

    class Meta:
        unique_together = ['id', 'nombre']
        ordering = ['id']

class Hexagono(models.Model):
    position = models.IntegerField(default=0)
    resource  = models.CharField(max_length=25)
    token = models.IntegerField(default= 0)
    tablero = models.ForeignKey(Tablero, related_name='hexagonos', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['tablero', 'token']
        ordering = ['token']

    def __str__(self):
        return '{resource: %s , token: %d}' % (self.resource, self.token)

class Vertice(models.Model):
    nivel = models.IntegerField(default= 0)
    indice = models.IntegerField(default= 0)
    tablero = models.ForeignKey(Tablero, related_name='vertices', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['nivel', 'indice']
        ordering = ['nivel']

    def __str__(self):
        return '{nivel: %d , indice: %d}' % (self.nivel, self.indice)