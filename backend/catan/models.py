from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from random import random, shuffle


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

    def is_full(self):
        return len(self.players.all()) == 4

    def start_game(self):
        players = self.players.all()
        desert_terrain = Hexe.objects.get(board=self.board_id,
                                          terrain='desert')
        hexes = Hexe.objects.filter(board=self.board_id)
        board = Board.objects.get(id=self.board_id)
        game = Game.objects.create(name=self.name,
                                   board=board,
                                   robber=desert_terrain)
        turns_colors = {1: 'Blue', 2: 'Red', 3: 'Yellow', 4: 'Green'}
        keys = list(turns_colors.keys())
        shuffle(keys)
        for key in keys:
            new_player = Player.objects.create(turn=key,
                                               username=players[key-1],
                                               game=game,
                                               colour=turns_colors[key])
            if key == 1:
                print(key)
                Current_Turn.objects.create(
                    game=game,
                    user=new_player.username,
                    game_stage='FIRST_CONSTRUCTION',
                    last_action='NON_BLOCKING_ACTION')
        self.game_has_started = True
        print(game.id)
        self.game_id = game.id
        self.save()

    def can_delete(self, owner):
        return (not self.game_has_started) and (self.owner == owner)


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
        ('Yellow', 'Yellow'),
        ('Blue', 'Blue'),
        ('Green', 'Green'),
        ('Red', 'Red'),
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
            models.UniqueConstraint(fields=['turn', 'game'],
                                    name='User with unique turn per game'),
            models.UniqueConstraint(fields=['colour', 'game'],
                                    name='User with unique colour per game'),
        ]

    def set_not_last_gained(self):
        """
        A method to remove resources as obtained in the last turn.
        """
        # Get the last gained of the owner
        resources_last_gained = Resource.objects.filter(last_gained=True,
                                                        owner=self.username)
        # Set the resources to False in last_gained field
        if len(resources_last_gained) != 0:
            for resource in resources_last_gained:
                resource.last_gained = False
                resource.save()

    def gain_resources(self, resource_name, amount):
        """
        A method for players to gain resources.
        Args:
        game: the game in which the owner is.
        owner: a player who will get the resources.
        resource_name: the type of resources to obtain.
        amount: the amount of resources to obtain.
        """
        for i in range(amount):
            Resource.objects.create(owner=self.owner, game=self.game,
                                    resource_name=resource_name,
                                    last_gained=True)


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
    name = models.CharField(max_length=6, choices=RESOURCE_TYPE)
    last_gained = models.BooleanField(default=False)

    def __str__(self):
        return self.resource_name

    def clean(self):
        if self.owner.game.id != self.game.id:
            raise ValidationError('Cannot be player of other game')

    def set_not_last_gained(self):
        """
        A method to remove resources as obtained in the last turn.
        """
        # Get the last gained of the owner
        resources_last_gained = Resource.objects.filter(last_gained=True,
                                                        owner=self.owner)
        # Set the resources to False in last_gained field
        if len(resources_last_gained) != 0:
            for resource in resources_last_gained:
                resource.last_gained = False
                resource.save()


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
    """
    Stores information about the state of a started game,
    the player who is playing at the moment, the dices values
    and if the robber has been moved. Related to :model `Game`
    and :model `auth.User`
    """
    GAME_STAGE = [
        ('FIRST_CONSTRUCTION', 'FIRST_CONSTRUCTION'),
        ('SECOND_CONSTRUCTION', 'SECOND_CONSTRUCTION'),
        ('FULL_PLAY', 'FULL_PLAY')
    ]
    ACTIONS = [
        ('BUILD_SETTLEMENT', 'BUILD_SETTLEMENT'),
        ('BUILD_ROAD', 'BUILD_ROAD'),
        ('NON_BLOCKING_ACTION', 'NON_BLOCKING_ACTION')
    ]
    game = models.OneToOneField(Game, related_name='current_turn',
                                on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="user")
    game_stage = models.CharField(max_length=50, choices=GAME_STAGE,
                                  default='FULL_PLAY')
    last_action = models.CharField(max_length=50, choices=ACTIONS,
                                   default='NON_BLOCKING_ACTION')
    dices1 = models.IntegerField(null=True,
                                 validators=[MinValueValidator(1),
                                             MaxValueValidator(6)],
                                 default=1)
    dices2 = models.IntegerField(null=True,
                                 validators=[MinValueValidator(1),
                                             MaxValueValidator(6)],
                                 default=1)
    robber_moved = models.BooleanField(default=False)

    def throw_dice(self):
        """
        A function to generate a thow of dice
        (uniform discrete distribution).
        """
        return 1 * int(6 * random()) + 1

    def throw_twoDices(self, dice1=0, dice2=0):
        """
        A function to get the throw of two dices
        Params:
        @dice1: the value of the dice1 (used only for testing).
        @dice2: the value of the dice2 (used only for testing).
        """
        if (dice1 == 0) and (dice2 == 0):
            self.dices1 = throw_dice()
            self.dices2 = throw_dice()
        else:
            return (dice1, dice2)
