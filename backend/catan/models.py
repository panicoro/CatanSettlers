from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


class HexePosition(models.Model):
    level = models.IntegerField(default=0,
                                validators=[MinValueValidator(0),
                                            MaxValueValidator(2)])
    index = models.IntegerField(default=0,
                                validators=[MinValueValidator(0),
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


class VertexPosition(models.Model):
    level = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                                       MaxValueValidator(2)])
    index = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                                       MaxValueValidator(29)])

    class Meta:
        unique_together = ['level', 'index']
        ordering = ['level']

    def clean(self):
        if (self.level == 0) and not (0 <= self.index <= 5):
            raise ValidationError(
                'The index with level 0 must be between 0 and 5.')
        if (self.level == 1) and not (0 <= self.index <= 17):
            raise ValidationError(
                'The index with level 1 must be between 0 and 17.')
        if (self.level == 2) and not (0 <= self.index <= 29):
            raise ValidationError(
                'The index with level 2 must be between 0 and 29.')


class Board(models.Model):
    name = models.CharField(max_length=25)

    class Meta:
        unique_together = ['id', 'name']
        ordering = ['id']


RESOURCE_TYPE = [
    ('brick', 'BRICK'),
    ('lumber', 'LUMBER'),
    ('wool', 'WOOL'),
    ('grain', 'GRAIN'),
    ('ore', 'ORE')
]


class Hexe(models.Model):
    TERRAIN_TYPE = [('desert', 'DESERT')] + RESOURCE_TYPE
    terrain = models.CharField(max_length=6, choices=TERRAIN_TYPE)
    token = models.IntegerField(default=0, validators=[MinValueValidator(2),
                                                       MaxValueValidator(12)])
    board = models.ForeignKey(Board, related_name='board_hexe',
                              on_delete=models.CASCADE)
    position = models.ForeignKey(HexePosition, related_name='hexe_position',
                                 on_delete=models.CASCADE)

    class Meta:
        unique_together = ['board', 'position']
        ordering = ['id']


class Room(models.Model):
    name = models.CharField(max_length=50)
    max_players = models.IntegerField(default=3,
                                      validators=[MinValueValidator(3),
                                                  MaxValueValidator(4)])
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    players = models.ManyToManyField(User, related_name='room_players',
                                     blank=True)

    def __str__(self):
        return '{}'.format(self.name)


class Game(models.Model):
    name = models.CharField(max_length=25)
    board = models.ForeignKey(Board, related_name='game_board',
                              on_delete=models.CASCADE)
    robber = models.ForeignKey(HexePosition, related_name="robber",
                               on_delete=models.CASCADE)
    winner = models.ForeignKey(User, related_name="game_winner",
                               on_delete=models.CASCADE,
                               blank=True, null=True)

    class Meta:
        unique_together = ['id', 'name']
        ordering = ['id']


class Player(models.Model):
    COLOUR = [
        ('yellow', 'YELLOW'),
        ('blue', 'BLUE'),
        ('green', 'GREEN'),
        ('red', 'RED'),
    ]
    turn = models.IntegerField(validators=[MinValueValidator(1),
                                           MaxValueValidator(4)])
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    colour = models.CharField(max_length=50, choices=COLOUR)

    development_cards = models.IntegerField(default=0,
                                            validators=[MinValueValidator(0)])
    resources_cards = models.IntegerField(default=0,
                                          validators=[MinValueValidator(0)])
    victory_points = models.IntegerField(default=0,
                                         validators=[MinValueValidator(0)])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['username', 'game'],
                                    name='User in one game at time'),
            models.UniqueConstraint(fields=['turn', 'game'],
                                    name='User with unique turn per game'),
            models.UniqueConstraint(fields=['colour', 'game'],
                                    name='User with unique colour per game'),
        ]

    def __str__(self):
        return '%s' % (self.username)


class Card(models.Model):
    CARD_TYPE = [
        ('road_building', 'ROAD_BUILDING'),
        ('year_of_plenty', 'YEAR_OF_PLENTY'),
        ('monopoly', 'MONOPOLY'),
        ('victory_point', 'VICTORY_POINT'),
        ('knight', 'KNIGHT')
    ]
    owner = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    card_name = models.CharField(max_length=50, choices=CARD_TYPE)

    def __str__(self):
        return self.card_name

    def clean(self):
        if self.owner.game.id != self.game.id:
            raise ValidationError('Cannot be player of other game')


class Resource(models.Model):
    owner = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    resource_name = models.CharField(max_length=6, choices=RESOURCE_TYPE)
    last_gained = models.BooleanField(default=False)

    def __str__(self):
        return self.resource_name

    def clean(self):
        if self.owner.game.id != self.game.id:
            raise ValidationError('Cannot be player of other game')


class Building(models.Model):
    TYPE_BUILDING = [
        ('SETTLEMENT', 'settlement'),
        ('CITY', 'city')
    ]
    game = models.ForeignKey(Game, on_delete=models.CASCADE,
                             related_name="building_game")
    name = models.CharField(max_length=50, choices=TYPE_BUILDING)
    owner = models.ForeignKey(Player, related_name='buildings',
                              on_delete=models.CASCADE)
    position = models.ForeignKey(VertexPosition, related_name='position',
                                 on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['position', 'game'],
                                    name='One building per position in game')
        ]

    def clean(self):
        if self.owner.game.id != self.game.id:
            raise ValidationError('Cannot be player of other game')


class Road(models.Model):
    owner = models.ForeignKey(Player, related_name='roads',
                              on_delete=models.CASCADE)
    vertex_1 = models.ForeignKey(VertexPosition, on_delete=models.CASCADE,
                                 related_name="vertex_position1")
    vertex_2 = models.ForeignKey(VertexPosition, on_delete=models.CASCADE,
                                 related_name="vertex_position2")
    game = models.ForeignKey(Game, on_delete=models.CASCADE,
                             related_name="road_game")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['vertex_1', 'vertex_2', 'game'],
                                    name='One Road per vertex in game')
            ]

    def clean(self):
        if self.owner.game.id != self.game.id:
            raise ValidationError('Cannot be player of other game')


class Current_Turn(models.Model):
    game = models.OneToOneField(Game, related_name='current_turn',
                                on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="user")
    dices1 = models.IntegerField(blank=True,
                                 validators=[MinValueValidator(1),
                                             MaxValueValidator(6)])
    dices2 = models.IntegerField(blank=True,
                                 validators=[MinValueValidator(1),
                                             MaxValueValidator(6)])
