from django.db import models

class Resource (models.Model):

    RESOURCE_TYPE = [
        ('BRICK','brick'),
        ('LUMBER','lumber'),
        ('WOOL','wool'),
        ('GRAIN','grain'),
        ('ORE','ore')
    ]
    name = models.CharField(max_length= 6, choices=RESOURCE_TYPE)
    quantity = models.IntegerField(default=0)
    