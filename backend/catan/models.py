from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from random import random, shuffle
from django.db.models import Q
from catan.cargaJson import VertexInfo

def generateHexesPositions():
    """
    A method to generate all the positions of the hexagons in the board:
    """
    positions = []
    top_ranges = [1, 6, 12]
    for i in range(0, 3):
        for j in range(0, top_ranges[i]):
            positions.append([i, j])            
    return positions

def generateVertexPositions():
    """
    A method to generate all the positions of the vertex in the board:
    Generate only one time.
    """
    positions = []
    top_ranges = [6, 18, 30]
    for i in range(0, 3):
        for j in range(0, top_ranges[i]):
            positions.append([i, j])
    return positions

VERTEX_POSITIONS = generateVertexPositions()


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

    def exists_building(self, level, index):
        """
        Return true is there's a bulding in the 
        vertex position with gaven level and index
        """
        return Building.objects.filter(game=self, level=level,
                                   index=index).exists()

    def check_not_building(self, level, index):
        """
        Returns True if there is no construction in the neighbors of the
        VertexPosition entered by the player.
        """
        list_build = Building.objects.filter(game=self)
        list_vertex = VertexInfo(level, index)
        for build in list_build:
            for vertex in list_vertex:
                if build.level == vertex[0] and \
                   build.index == vertex[1]:
                    return False              
        return True

    def posibles_initial_settlements(self):
        """
        A function that obtains positions that the players might have
        available to build settlements on the board during the
        construction stage of a started game
        """
        vertex_available = VERTEX_POSITIONS
        # Get all the buildings
        buildings = Building.objects.filter(game=self)
        if len(buildings) == 0:
            return vertex_available
        else:
            for building in buildings:
                building_vertex = [building.level, building.index]
                if building_vertex in vertex_available:
                    vertex_available.remove(building_vertex)
                neighbors = VertexInfo(building.level, building.index)
                for neighbor in neighbors:
                    if neighbor in vertex_available:
                        vertex_available.remove(neighbor)
            return vertex_available


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

    NECESSARY_RESOURCES = {'Settlement': ['brick', 'lumber', 'wool', 'grain'],
                           'Road': ['brick', 'lumber']
                          }

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
        # Get the last gained of the player
        resources_last_gained = Resource.objects.filter(last_gained=True,
                                                        owner=self)
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
        print(self)
        for i in range(amount):
            Resource.objects.create(owner=self, game=self.game,
                                    name=resource_name,
                                    last_gained=True)

    def has_necessary_resources(self, action):
        NECESSARY_RESOURCES = {'build_settlement': ['brick', 'lumber',
                                                    'wool', 'grain'],
                               'build_road': ['brick', 'lumber']
                               }
        needed_resources = NECESSARY_RESOURCES[action]
        for resource in needed_resources:
            resource_exists  = Resource.objects.filter(owner=self,
                                                       name=resource).exists()
            if (not resource_exists):
                return False
        return True

    def delete_resources(self, action):
        """
        Remove resources from the list.
        """
        NECESSARY_RESOURCES = {'build_settlement': ['brick', 'lumber',
                                                    'wool', 'grain'],
                               'build_road': ['brick', 'lumber']
                               }
        used_resources = NECESSARY_RESOURCES[action]
        for resource in used_resources:
            Resource.objects.get(owner=self, name=resource).delete()
    
    def check_my_road(self, level, index):
        """
        Returns True if there is one of the vertices of the player's paths
        matches the VertexPosition entered by it.
        """
        return Road.objects.filter(Q(owner=self, game=self.game,
                                   level_1=level, index_1=index) |
                                   Q(owner=self, game=self.game,
                                   level_2=level, index_2=index)).exists()

    def get_my_roads_and_buildings(self):
        """
        A function that obtains two set of vertex positions of
        the roads and buildings of a given player.
        Args:
        """
        roads = Road.objects.filter(owner=self)
        vertex_roads = set()
        for road in roads:
            vertex = (road.level_1, road.index_1) 
            vertex_roads.add(vertex)
            vertex = (road.level_2, road.index_2)
            vertex_roads.add(vertex)
        buildings = Building.objects.filter(owner=self)
        vertex_buildings = set()
        for build in buildings:
            vertex = (build.level, build.index)
            vertex_buildings.add(vertex)
        return (vertex_roads, vertex_buildings)

    def posibles_settlements(self):
        """
        A function that obtains positions that a player might have
        available to build settlements on the board.
        Args:
        """
        (vertex_roads, vertex_buildings) = self.get_my_roads_and_buildings()
        # I get the vertices of my own roads that are not occupied by my buildings
        available_vertex = vertex_roads - vertex_buildings
        potencial_buildings = list(available_vertex)
        potencial_buildings = [[pos[0], pos[1]] for pos in potencial_buildings]
        available_vertex = [[pos[0], pos[1]] for pos in available_vertex]
        # For each vertices check that their neighbors are not occupied,
        # if they are it can not be built (distance rule)
        for vertex in available_vertex:
        # Get the neighbors of a vertex position
            neighbors = VertexInfo(vertex[0], vertex[1])
            for neighbor in neighbors:
                # If there a building in one of the neighbors then
                # the vertex couldn't have a new building...
                if Building.objects.filter(level=neighbor[0], 
                                           index=neighbor[1]).exists():
                    potencial_buildings.remove(vertex)
                    break
        return potencial_buildings

    def is_winner(self):
        points = self.victory_points
        card_vic_points = Card.objects.filter(game=self.game, owner=self,
                                              card_name='victory_point').count()
        total = points + card_vic_points
        if total != 10:
            return False
        user = User.objects.get(username=self.username)
        self.game.winner = user
        self.game.save()
        return True
        
    def gain_points(self, amount):
        self.victory_points += amount
        self.save()
    


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
