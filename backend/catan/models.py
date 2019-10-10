from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Board(models.Model):
    name = models.CharField(max_length=25, blank=True, default='')

    class Meta:
        unique_together = ['id', 'name']
        ordering = ['id']

class Game(models.Model):
    name = models.CharField(max_length=25)
    in_turn = models.CharField(max_length=25)
    board = models.ForeignKey(Board, related_name='games', on_delete=models.CASCADE)
    class Meta:
        unique_together = ['id', 'name']
        ordering = ['id']

    def __str__(self):
        return '{name: %s , in_turn: %s}' % (self.name, self.in_turn)

class Hexes(models.Model):

    POSITION_AVAILABLES = [
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

    position = models.CharField(max_length=2, choices=POSITION_AVAILABLES)
    resource  = models.CharField(max_length=25)
    token = models.IntegerField(default= 0)
    board = models.ForeignKey(Board, related_name='hexes', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['board', 'position']
        ordering = ['token']

    def __str__(self):
        return '{position:{%s} ,resource: %s , token: %d}' % (self.position, self.resource, self.token)

class Vertex(models.Model):
    level = models.IntegerField(default= 0)
    index = models.IntegerField(default= 0)
    board = models.ForeignKey(Board, related_name='vertex', on_delete=models.CASCADE)

    class Meta:
        unique_together = ['level', 'index']
        ordering = ['level']

    def __str__(self):
        return '{level: %d , index: %d}' % (self.level, self.index)

class VertexPosition(models.Model):
    level = models.IntegerField(default= 0)
    index = models.IntegerField(default= 0)
    
    class Meta:
        unique_together = ['level', 'index']
        ordering = ['level']

    def __str__(self):
        return '{level: %d , index: %d}' % (self.level, self.index)