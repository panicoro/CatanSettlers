from django.db import models
from django.contrib.auth.models import User


class Game(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return '%s' % (self.order, self.name)

class Player(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game,related_name='players',on_delete = models.CASCADE)

    def __str__(self):
        return '%s' % (self.username)

class Resource(models.Model):

    RESOURCE_TYPE = [
        ('BRICK','brick'),
        ('LUMBER','lumber'),
        ('WOOL','wool'),
        ('GRAIN','grain'),
        ('ORE','ore')
    ]
    name = models.CharField(max_length= 6, choices=RESOURCE_TYPE)
    owner = models.ForeignKey(Player, on_delete=models.CASCADE)