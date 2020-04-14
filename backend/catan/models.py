from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError


class Room(models.Model):
    """
    Stores information about one lobby of the game, ralated to
    :model: `auth.User`
    """
    name = models.CharField(max_length=50)
    max_players = models.IntegerField(default=4,
                                      validators=[MinValueValidator(4),
                                                  MaxValueValidator(4)])
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    players = models.ManyToManyField(User, related_name='room_players',
                                     blank=True)
    game_id = models.IntegerField(null=True, blank=True)
    board_id = models.IntegerField()
    game_has_started = models.BooleanField(default=False)


class Board(models.Model):
    name = models.CharField(max_length=15)

    class Meta:
        unique_together = ['id', 'name']
        ordering = ['id']


"""
An array of tuples that contains the type of resources need
for cards and types of terrains.
"""
RESOURCE_TYPE = [
    ('brick', 'BRICK'),
    ('lumber', 'LUMBER'),
    ('wool', 'WOOL'),
    ('grain', 'GRAIN'),
    ('ore', 'ORE')
]


class Hexe(models.Model):
    """
    Stores information about one hexagon of the board game,
    related to :model `Board`
    """
    TERRAIN_TYPE = [('desert', 'DESERT')] + RESOURCE_TYPE
    terrain = models.CharField(max_length=6, choices=TERRAIN_TYPE)
    token = models.IntegerField(default=0, validators=[MinValueValidator(2),
                                                       MaxValueValidator(12)])
    board = models.ForeignKey(Board, related_name='board_hexe',
                              on_delete=models.CASCADE)
    level = models.IntegerField(default=0,
                                validators=[MinValueValidator(0),
                                            MaxValueValidator(2)])
    index = models.IntegerField(default=0,
                                validators=[MinValueValidator(0),
                                            MaxValueValidator(11)])

    class Meta:
        unique_together = ['board', 'level', 'index']
        ordering = ['id']

    def clean(self):
        """
        Check if the values of levels and index are correct
        according to the board diposition.
        """
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
    """
    Stores the information about an started game, related to
    :model `Hexe` and :model `auth.User`
    """
    name = models.CharField(max_length=15)
    board = models.ForeignKey(Board, related_name='game_board',
                              on_delete=models.CASCADE)
    robber = models.ForeignKey(Hexe, related_name="robber",
                               on_delete=models.CASCADE)
    winner = models.ForeignKey(User, related_name="game_winner",
                               on_delete=models.CASCADE,
                               blank=True, null=True)

    class Meta:
        unique_together = ['id', 'name']
        ordering = ['id']


class Player(models.Model):
    """
    Stores information about a player of a started game,
    related to :model `auth.User` and :model `Game`
    """
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


class Card(models.Model):
    '''
    Stores information about a card of a player in a started game,
    related to :model `Game` and :model `Player`
    '''
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

    def clean(self):
        '''
        Check if the owner of a card is in the same game
        '''
        if self.owner.game.id != self.game.id:
            raise ValidationError('Cannot be player of other game')


class Resource(models.Model):
    """
    Stores information about a resource of a player in a started game,
    related to :model `Player` and :model `Game`
    """
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
    """
    Stores information about a building of a player in a started game,
    related to :model `Player` and :model `Game`
    """
    TYPE_BUILDING = [
        ('settlement', 'SETTLEMENT'),
        ('city', 'CITY')
    ]
    game = models.ForeignKey(Game, on_delete=models.CASCADE,
                             related_name="building_game")
    name = models.CharField(max_length=50, choices=TYPE_BUILDING)
    owner = models.ForeignKey(Player, related_name='buildings',
                              on_delete=models.CASCADE)
    level = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                                       MaxValueValidator(2)])
    index = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                                       MaxValueValidator(29)])

    class Meta:
        unique_together = ['level', 'index', 'game']
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
        if self.owner.game.id != self.game.id:
            raise ValidationError('Cannot be player of other game')


class Road(models.Model):
    """
    Stores information about road of a player in a started game,
    related to :model `Player` and :model `Game`
    """
    owner = models.ForeignKey(Player, related_name='roads',
                              on_delete=models.CASCADE)
    level_1 = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                                         MaxValueValidator(2)])
    index_1 = models.IntegerField(default=0,
                                  validators=[MinValueValidator(0),
                                              MaxValueValidator(29)])
    level_2 = models.IntegerField(default=0,
                                  validators=[MinValueValidator(0),
                                              MaxValueValidator(2)])
    index_2 = models.IntegerField(default=0,
                                  validators=[MinValueValidator(0),
                                              MaxValueValidator(29)])
    game = models.ForeignKey(Game, on_delete=models.CASCADE,
                             related_name="road_game")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['level_1', 'index_1',
                                            'level_2', 'index_2', 'game'],
                                    name='One Road per vertex in game')
            ]

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
        if self.owner.game.id != self.game.id:
            raise ValidationError('Cannot be player of other game')
        if self.owner.game.id != self.game.id:
            raise ValidationError('Cannot be player of other game')


class Current_Turn(models.Model):
    game = models.OneToOneField(Game, related_name='current_turn',
                                on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="user")
    dices1 = models.IntegerField(null=True,
                                 validators=[MinValueValidator(1),
                                             MaxValueValidator(6)])
    dices2 = models.IntegerField(null=True,
                                 validators=[MinValueValidator(1),
                                             MaxValueValidator(6)])
    robber_moved = models.BooleanField(default=False)
