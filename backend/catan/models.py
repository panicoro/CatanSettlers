from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Game(models.Model):
    name = models.CharField(max_length=25)
    in_turn = models.ForeignKey(User, related_name='in_turn',
                                on_delete=models.CASCADE, null=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE,
                               blank=True, null=True)
    roober = models.IntegerField()

    class Meta:
        unique_together = ['id', 'name']
        ordering = ['id']


class Player(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    colour = models.CharField(max_length=50)
    development_cards = models.IntegerField(default=0,
                                            validators=[MinValueValidator(0)])
    resources_cards = models.IntegerField(default=0,
                                          validators=[MinValueValidator(0)])

    def __str__(self):
        return '%s' % (self.username)


class Resource(models.Model):
    RESOURCE_TYPE = [
        ('BRICK', 'brick'),
        ('LUMBER', 'lumber'),
        ('WOOL', 'wool'),
        ('GRAIN', 'grain'),
        ('ORE', 'ore')
    ]

    owner = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    resource_name = models.CharField(max_length=6, choices=RESOURCE_TYPE)

    def __str__(self):
        return self.resource_name


class Card(models.Model):
    CARD_TYPE = [
        ('ROAD_BUILDING', 'road_building'),
        ('YEAR_OF_PLENTY', 'year_of_plenty'),
        ('MONOPOLY', 'monopoly'),
        ('VICTORY_POINT', 'victory_point'),
        ('KNIGHT', 'knight')
    ]
    owner = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    card_name = models.CharField(max_length=50, choices=CARD_TYPE)

    def __str__(self):
        return self.card_name
