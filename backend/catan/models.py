from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


class Board(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        unique_together = ['id', 'name']
        ordering = ['id']


class HexePosition(models.Model):
    level = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                                       MaxValueValidator(2)])
    index = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                                       MaxValueValidator(11)])

    class Meta:
        unique_together = ['level', 'index']
        ordering = ['level']

    def clean(self):
        if (self.level == 0) and not (0 <= self.index <= 0):
            raise ValidationError(
                'The index with level 0 must be between 0 and 0.')
        if (self.level == 1) and not (0 <= self.index <= 5):
            raise ValidationError(
                'The index with level 1 must be between 0 and 5.')
        if (self.level == 2) and not (0 <= self.index <= 11):
            raise ValidationError(
                'The index with level 2 must be between 0 and 11.')


class Game(models.Model):
    name = models.CharField(max_length=25)
    board = models.ForeignKey(Board, related_name='game_board',
                              on_delete=models.CASCADE)
    roober = models.ForeignKey(HexePosition, related_name="robber",
                               on_delete=models.CASCADE)
    winner = models.ForeignKey(User, related_name="game_winner",
                               on_delete=models.CASCADE,
                               blank=True, null=True)

    class Meta:
        unique_together = ['id', 'name']
        ordering = ['id']


RESOURCE_TYPE = [
    ('brick', 'BRICK'),
    ('lumber', 'LUMBER'),
    ('wool', 'WOOL'),
    ('grain', 'GRAIN'),
    ('ore', 'ORE'),
]


class Hexe(models.Model):
    TERRAIN_TYPE = [('desert', 'DESERT')] + RESOURCE_TYPE
    terrain = models.CharField(max_length=6, choices=TERRAIN_TYPE)
    token = models.IntegerField(default=0, validators=[MinValueValidator(2),
                                                       MaxValueValidator(12)])
    board = models.ForeignKey(Board, related_name='hexe_board',
                              on_delete=models.CASCADE)
    position = models.ForeignKey(HexePosition, related_name='hexe_position',
                                 on_delete=models.CASCADE)
