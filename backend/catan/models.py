from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class Room(models.Model):
    name = models.CharField(max_length=50)
    max_players = models.IntegerField(default=3,
                                      validators=[MinValueValidator(3),
                                                  MaxValueValidator(4)])
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    players = models.ManyToManyField(User, related_name='room_players',
                                     blank=True)
