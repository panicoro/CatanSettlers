from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Player(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
#   game = models.ForeignKey(Game, on_delete=models.CASCADE)
    colour = models.CharField(max_length=50)
    development_cards = models.IntegerField(default=0,
                                            validators=[MinValueValidator(0)])
    resources_cards = models.IntegerField(default=0,
                                          validators=[MinValueValidator(0)])

    def __str__(self):
        return '%s' % (self.username)


class Card(models.Model):
    CARD_TYPE = [
        ('ROAD_BUILDING', 'road_building'),
        ('YEAR_OF_PLENTY', 'year_of_plenty'),
        ('MONOPOLY', 'monopoly'),
        ('VICTORY_POINT', 'victory_point'),
        ('KNIGHT', 'knight')
    ]
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    card_name = models.CharField(max_length=50, choices=CARD_TYPE)

    def __str__(self):
        return self.card_name


class Resource(models.Model):
    RESOURCE_TYPE = [
        ('BRICK', 'brick'),
        ('LUMBER', 'lumber'),
        ('WOOL', 'wool'),
        ('GRAIN', 'grain'),
        ('ORE', 'ore')
    ]
    resource_name = models.CharField(max_length=6, choices=RESOURCE_TYPE)
    owner = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return self.resource_name


class Vertex_position_settlements(models.Model):
    player = models.ForeignKey(Player, related_name='settlements',
                               on_delete=models.CASCADE)
    level = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                MaxValueValidator(2)])
    index = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                MaxValueValidator(29)])

    def __str__(self):
        return '(%d, %d)' % (self.level, self.index)


class Vertex_position_cities(models.Model):
    player = models.ForeignKey(Player, related_name='cities',
                               on_delete=models.CASCADE)
    level = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                MaxValueValidator(2)])
    index = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                MaxValueValidator(29)])

    def __str__(self):
        return '(%d, %d)' % (self.level, self.index)


class Road_position(models.Model):
    player = models.ForeignKey(Player, related_name='roads',
                               on_delete=models.CASCADE)
    level1 = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                 MaxValueValidator(2)])
    index1 = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                 MaxValueValidator(29)])
    level2 = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                 MaxValueValidator(2)])
    index2 = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                 MaxValueValidator(29)])

    def __str__(self):
        return '((%d, %d),(%d, %d))' % (self.level1, self.index1,
                                        self.level2, self.index2)


class Last_gained(models.Model):
    player = models.ForeignKey(Player, related_name='last_gained',
                               on_delete=models.CASCADE, null=True)
    resources = models.ForeignKey(Resource, on_delete=models.CASCADE,
                                  null=True, blank=True)

    def __str__(self):
        return '%s' % (self.resources)
