from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from random import random, shuffle, randint
from django.db.models import Q
import math
from aux.json_load import VertexInfo, HexagonInfo


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
HEXE_POSITIONS = generateHexesPositions()


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

"""
An array of tuples that contains the diferent types of cards.
"""
CARD_TYPE = [
        ('road_building', 'ROAD_BUILDING'),
        ('year_of_plenty', 'YEAR_OF_PLENTY'),
        ('monopoly', 'MONOPOLY'),
        ('victory_point', 'VICTORY_POINT'),
        ('knight', 'KNIGHT')
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

    def exists_road(self, level1, index1, level2, index2):
        road_1 = Road.objects.filter(game=self,
                                     level_1=level1, level_2=level2,
                                     index_1=index1, index_2=index2
                                     ).exists()
        road_2 = Road.objects.filter(game=self,
                                     level_2=level1, level_1=level2,
                                     index_2=index1, index_1=index2
                                     ).exists()
        return road_1 or road_2

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

    def move_robber(self, level, index):
        hexe_robber = Hexe.objects.filter(board=self.board,
                                          level=level,
                                          index=index).get()
        self.robber = hexe_robber
        self.save()
        self.current_turn.robber_moved = True
        self.current_turn.save()

    def robber_has_been_moved(self):
        return self.current_turn.robber_moved

    def is_new_robber_position(self, level, index):
        return (self.robber.level != level) or (self.robber.index != index)

    def get_sum_dices(self):
        return sum(self.current_turn.get_dices())

    def set_players_resources_not_last_gained(self):
        """
        A method to set the resources of a list of players
        as not last gained.
        """
        players = Player.objects.filter(game=self)
        for player in players:
            player.set_not_last_gained()

    def random_discard(self):
        players = Player.objects.filter(game=self)
        for player in players:
            if len(Resource.objects.filter(owner=player)) > 7:
                resources = Resource.objects.filter(owner=player)
                res_pos = [i for i in range(0, len(resources))]
                shuffle(res_pos)
                res_pos = res_pos[0:math.floor(len(res_pos)/2)]
                for elem in res_pos:
                    resources[elem].delete()

    def distribute_resources(self, hexes):
        """
        A method that takes a list of hexagons and a list of players.
        For each hex on the list, check if each player on the list has
        buildings at the vertices of that hex; if the player has them
        increases his amount of resources.
        Params:
        @hexes: a list of selected objects Hexes of the board.
        @players: a list of players of a started game.
        @game: a started game.
        """
        players = Player.objects.filter(game=self)
        if len(hexes) != 0:
            for hexe in hexes:
                hexe_level = hexe.level
                hexe_index = hexe.index
                hexe_neighbors = HexagonInfo(hexe_level, hexe_index)
                for player in players:
                    # get the buildings of the player
                    buildings = Building.objects.filter(owner=player)
                    if len(buildings) != 0:
                        for building in buildings:
                            building_vertex = [building.level,
                                               building.index]
                            if building_vertex in hexe_neighbors:
                                if building.name == 'settlement':
                                    player.gain_resources(hexe.terrain, 1)
                                else:
                                    player.gain_resources(hexe.terrain, 2)

    def throw_dices(self, dice1=0, dice2=0):
        """
        A method that rolls the two dice at the begin of the turn and
        distributes the resources according to the hexagons with the
        token of the sum of the dice.
        Params:
        @dice1: the value of the dice1 (used only for testing).
        @dice2: the value of the dice2 (used only for testing).
        """
        # Get the trow of dices and then sum them.
        two_dices = self.current_turn.throw_two_dices(dice1, dice2)
        sum_dices = sum(two_dices)
        # Get the players of the games
        if sum_dices == 7:
            self.random_discard()
        else:
            self.set_players_resources_not_last_gained()
            # Get the hexes with this token from the board
            hexes = Hexe.objects.filter(board=self.board, token=sum_dices)
            # If the robber is in one hexes with the token of the sum
            # then we must exclude it...
            if hexes.filter(id=self.robber.id).exists():
                hexes = hexes.exclude(id=self.robber.id)
            # Then distribute_resources...
            self.distribute_resources(hexes)

    def can_change_turn(self):
        game_stage = self.current_turn.game_stage
        last_action = self.current_turn.last_action
        if game_stage != 'FULL_PLAY':
            if last_action != 'BUILD_ROAD':
                return False
        return True

    def change_turn(self):
        self.current_turn.set_new_turn()

    def check_player_in_turn(self, player):
        """
        A method to check if the player is in turn in the given game.
        Args:
        @game: a started game.
        @player: a player in the game.
        """
        return self.current_turn.user == player.username


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
            Resource.objects.create(owner=self, game=self.game,
                                    name=resource_name,
                                    last_gained=True)

    def gain_resources_free(self, position):
        """
        """
        hexes = Hexe.objects.filter(board=self.game.board)
        for hexe in hexes:
            hexe_level = hexe.level
            hexe_index = hexe.index
            hexagon_neighbors = HexagonInfo(hexe_level, hexe_index)
            if position in hexagon_neighbors:
                self.gain_resources(hexe.terrain, 1)

    def has_necessary_resources(self, action, gaven=''):
        """
        A method to check is the player has necessary resources for
        do the desired action.
        Args:
        @action: the action of the player
        @gave: optional, only used if the action is 'trade_bank'.
               It's the type of resource that the player want to get.
        """
        NECESSARY_RESOURCES = {'build_settlement': ['brick', 'lumber',
                                                    'wool', 'grain'],
                               'build_road': ['brick', 'lumber'],
                               'buy_card': ['ore', 'grain', 'wool']
                               }
        if gaven:
            return Resource.objects.filter(owner=self,
                                           name=gaven).count() >= 4
        needed_resources = NECESSARY_RESOURCES[action]
        for resource in needed_resources:
            resource_exists = Resource.objects.filter(owner=self,
                                                      name=resource).exists()
            if (not resource_exists):
                return False
        return True

    def can_trade_bank(self):
        for resource in RESOURCE_TYPE:
            if self.has_necessary_resources('trade_bank', resource[0]):
                return True
        return False

    def delete_resources(self, action, gaven=''):
        """
        A method to delete the  necessary resources for
        do the desired action.
        Args:
        @action: the action of the player
        @gave: optional, only used if the action is 'trade_bank'.
               It's the type of resource that the player want to get.
        """
        NECESSARY_RESOURCES = {'build_settlement': ['brick', 'lumber',
                                                    'wool', 'grain'],
                               'build_road': ['brick', 'lumber'],
                               'trade_bank': [gaven for resource in range(4)],
                               'buy_card': ['ore', 'grain', 'wool']
                               }
        used_resources = NECESSARY_RESOURCES[action]
        for resource in used_resources:
            Resource.objects.filter(owner=self, name=resource)[0].delete()

    def check_my_road(self, level, index):
        """
        Returns True if there is one of the vertices of the player's paths
        matches the VertexPosition entered by it.
        """
        return Road.objects.filter(Q(owner=self, game=self.game,
                                   level_1=level, index_1=index) |
                                   Q(owner=self, game=self.game,
                                   level_2=level, index_2=index)).exists()

    def check_roads_continuation(self, level1, index1, level2, index2):
        road_1 = Road.objects.filter(Q(owner=self, game=self.game,
                                     level_1=level1, index_1=index1) |
                                     Q(owner=self, game=self.game,
                                     level_2=level1, index_2=index1)
                                     ).exists()
        road_2 = Road.objects.filter(Q(owner=self, game=self.game,
                                     level_1=level2, index_1=index2) |
                                     Q(owner=self, game=self.game,
                                     level_2=level2, index_2=index2)
                                     ).exists()
        building_1 = Building.objects.filter(owner=self, game=self.game,
                                             level=level1, index=index1
                                             ).exists()
        building_2 = Building.objects.filter(owner=self, game=self.game,
                                             level=level2, index=index2
                                             ).exists()
        return road_1 or road_2 or building_1 or building_2

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
        # I get the vertices of my own roads that are not occupied by
        # my buildings
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

    def get_potencial_roads(self, available_vertex):
        """
        A function that receives a list of available vertices and
        returns a list of positions (ROAD_POSITIONS) in which roads
        can be constructed from the vertices given in the list
        Args:
        @avalaible_vertex: a list of vertex positions (objects)
        """
        potencial_roads = []
        for vertex in available_vertex:
            vertex = list(vertex)
            # Get the neighbors of a vertex
            neighbors = VertexInfo(vertex[0], vertex[1])
            for neighbor in neighbors:
                if not Road.objects.filter(Q(level_1=vertex[0],
                                             index_1=vertex[1],
                                             level_2=neighbor[0],
                                             index_2=neighbor[1]) |
                                           Q(level_2=vertex[0],
                                             index_2=vertex[1],
                                             level_1=neighbor[0],
                                             index_1=neighbor[1])).exists():
                    new_road = [vertex, neighbor]
                    potencial_roads.append(new_road)
        return potencial_roads

    def posible_roads(self):
        """
        A function that obtains positions that a player might have
        available to build roads on the board.
        Args:
        """
        (vertex_roads, vertex_buildings) = self.get_my_roads_and_buildings()
        available_vertex = vertex_buildings.union(vertex_roads)
        potencial_roads = self.get_potencial_roads(available_vertex)
        return potencial_roads

    def posibles_initial_roads(self):
        building = Building.objects.filter(owner=self).last()
        potencial_roads = []
        vertex = [building.level, building.index]
        neighbors = VertexInfo(vertex[0], vertex[1])
        for neighbor in neighbors:
            vertex_position = [neighbor[0], neighbor[1]]
            new_road = [vertex, vertex_position]
            potencial_roads.append(new_road)
        return potencial_roads

    def posibles_roads_card_road_building(self):
        """
        A function that obtains posistions that a player might have
        available to build the two roads using the Card road_building
        Args:
        @player: a player of a started game.
        """
        potencial_roads = self.posible_roads()
        new_positions = []
        for road in potencial_roads:
            new_positions.append(road[1])
        new_potencial_roads = self.get_potencial_roads(new_positions)
        total_roads = potencial_roads + new_potencial_roads
        # Remove the repeat road
        final_roads = total_roads
        for road in total_roads:
            invert_road = [road[1], road[0]]
            if invert_road in final_roads:
                final_roads.remove(invert_road)
        return final_roads

    def is_winner(self):
        points = self.victory_points
        card_vic_points = Card.objects.filter(game=self.game, owner=self,
                                              name='victory_point'
                                              ).count()
        total = points + card_vic_points
        if total < 10:
            return False
        user = User.objects.get(username=self.username)
        self.game.winner = user
        self.game.save()
        return True

    def gain_points(self, amount):
        self.victory_points += amount
        self.save()

    def select_card(self):
        card_name = CARD_TYPE[randint(0, 4)]
        new_card = Card(owner=self, game=self.game, name=card_name[0])
        new_card.save()

    def has_card(self, type_card):
        return Card.objects.filter(owner=self, name=type_card).exists()

    def get_players_to_steal(self, level, index):
        owners = set()
        neighbors = HexagonInfo(level, index)
        for neighbor in neighbors:
            if Building.objects.filter(level=neighbor[0],
                                       index=neighbor[1],
                                       game=self.game).exists():
                owner = Building.objects.get(level=neighbor[0],
                                             index=neighbor[1],
                                             game=self.game).owner
                if owner.username != self.username:
                    owners.add(Building.objects.get(level=neighbor[0],
                                                    index=neighbor[1]
                                                    ).owner.username.username)
        return list(owners)

    def use_card(self, card_type):
        Card.objects.filter(owner=self, name=card_type)[0].delete()

    def steal_to(self, choosen_player):
        user_to_steal = User.objects.get(username=choosen_player)
        player_to_steal = Player.objects.get(username=user_to_steal,
                                             game=self.game)
        resources_list = Resource.objects.filter(owner=player_to_steal)
        if len(resources_list) != 0:
            resource_to_steal = resources_list[randint(0,
                                               len(resources_list)-1)]
            resource_to_steal.owner = self
            resource_to_steal.last_gained = True
            resource_to_steal.save()

    def set_not_last_gained(self):
        """
        A method to remove resources as obtained in the last turn.
        Args:
        owner: the player who owns the resources.
        """
        # Get the last gained of the owner
        resources_last_gained = Resource.objects.filter(last_gained=True,
                                                        owner=self)
        # Set the resources to False in last_gained field
        if len(resources_last_gained) != 0:
            for resource in resources_last_gained:
                resource.last_gained = False
                resource.save()


class Card(models.Model):
    '''
    Stores information about a card of a player in a started game,
    related to :model `Game` and :model `Player`
    '''
    owner = models.ForeignKey(Player, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, choices=CARD_TYPE + RESOURCE_TYPE)

    def clean(self):
        '''
        Check if the owner of a card is in the same game
        '''
        if self.owner.game.id != self.game.id:
            raise ValidationError('Cannot be player of other game')


class Resource(Card):
    """
    Stores information about a resource of a player in a started game,
    related to :model `Player` and :model `Game`
    """
    last_gained = models.BooleanField(default=False)


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
        levels_indexs = [(self.level_1, self.index_1),
                         (self.level_2, self.index_2)]
        for level_index in levels_indexs:
            if (level_index[0] == 0) and not (0 <= level_index[1] <= 5):
                raise ValidationError(
                    'The index with level 0 must be between 0 and 5.')
            if (level_index[0] == 1) and not (0 <= level_index[1] <= 17):
                raise ValidationError(
                    'The index with level 1 must be between 0 and 17.')
            if (level_index[0] == 2) and not (0 <= level_index[1] <= 29):
                raise ValidationError(
                    'The index with level 2 must be between 0 and 29.')
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

    def throw_two_dices(self, dice1=0, dice2=0):
        """
        A function to get the throw of two dices
        Params:
        @dice1: the value of the dice1 (used only for testing).
        @dice2: the value of the dice2 (used only for testing).
        """
        if (dice1 == 0) and (dice2 == 0):
            self.dices1 = self.throw_dice()
            self.dices2 = self.throw_dice()
            self.save()
            return self.get_dices()
        else:
            return (dice1, dice2)

    def get_dices(self):
        return (self.dices1, self.dices2)

    def set_new_turn(self):
        """
        A method to set a new player in turn on a given
        current turn of a started game.
        Args:
        @current_turn: a Current_Turn object of a started game.
        @ player: a player to set as new in the turn.
        """
        new_player = self.get_next_player()
        self.user = new_player.username
        self.last_action = 'NON_BLOCKING_ACTION'
        self.robber_moved = False
        self.save()

    def get_next_player(self):
        """
        A method to get the next player in the turn of a
        started game.
        Args:
        @current_turn: a Current_Turn object of a started game.
        @players: a queryset of the players of a started game.
        """
        player_in_turn = Player.objects.get(username=self.user,
                                            game=self.game)
        # Get the number of the actual turn
        actual_turn = player_in_turn.turn
        # Calculate the next turn in the game...
        # In the stage 'FIRST_CONSTRUCTION' and 'FULL_PLAY' the order
        # is the natural, and in the stage 'SECOND_CONSTRUCTION' the order
        # is the inverse
        game_stage = self.game_stage
        if game_stage == 'FIRST_CONSTRUCTION':
            if actual_turn != 4:
                next_turn = actual_turn + 1
            else:
                next_turn = actual_turn
                self.game_stage = 'SECOND_CONSTRUCTION'
                self.save()
        elif game_stage == 'SECOND_CONSTRUCTION':
            if actual_turn != 1:
                next_turn = actual_turn - 1
            else:
                next_turn = actual_turn
                self.game_stage = 'FULL_PLAY'
                self.game.throw_dices()
                self.save()
        else:
            if actual_turn == 4:
                next_turn = 1
            else:
                next_turn = actual_turn + 1
        # Get the player with the next turn
        next_player = Player.objects.get(turn=next_turn,
                                         game=self.game)
        return next_player
