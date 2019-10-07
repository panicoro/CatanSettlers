from django.db import models

class Tablero(models.Model):
    nombre = models.CharField(max_length=25, blank=True, default='')

    class Meta:
        unique_together = ['id', 'nombre']
        ordering = ['id']

class Hexagono(models.Model):
    COORDENADAS_AVAILABLES = [
            ('1','(0, 0)'),    
            ('2','(1, 0)'),
            ('3','(1, 1)'),
            ('4','(1, 2)'),
            ('5','(1, 3)'),
            ('6','(1, 4)'), 
            ('7','(1, 5)'),
            ('8','(2, 0)'),
            ('9','(2, 1)'),
            ('10','(2, 2)'),
            ('11','(2, 3)'),
            ('12','(2, 4)'), 
            ('13','(2, 5)'),
            ('14','(2, 6)'),
            ('15','(2, 7)'),
            ('16','(2, 8)'),
            ('17','(2, 9)'),
            ('18','(2, 10'),
            ('19','(2, 11'),
    ]
    position = models.CharField(max_length=2, choices=COORDENADAS_AVAILABLES)
    resource  = models.CharField(max_length=25)
    token = models.IntegerField(default= 0)
    tablero = models.ForeignKey(Tablero, related_name='hexagonos', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['tablero', 'position']
        ordering = ['token']

    def __str__(self):
        return '{position: %s, resource: %s , token: %d}' % (self.position, self.resource, self.token)

class Vertice(models.Model):
    nivel = models.IntegerField(default= 0)
    indice = models.IntegerField(default= 0)
    tablero = models.ForeignKey(Tablero, related_name='vertices', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['nivel', 'indice']
        ordering = ['nivel']

    def __str__(self):
        return '{nivel: %d , indice: %d}' % (self.nivel, self.indice)