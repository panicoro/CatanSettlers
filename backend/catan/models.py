from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    auto_increment_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length=50)



class Resource (models.Model):

    RESOURCE_TYPE = [
        ('BRICK','brick'),
        ('LUMBER','lumber'),
        ('WOOL','wool'),
        ('GRAIN','grain'),
        ('ORE','ore')
    ]
    name = models.CharField(max_length= 6, choices=RESOURCE_TYPE)

    