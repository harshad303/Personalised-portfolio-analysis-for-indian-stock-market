from django.db import models

# Create your models here.
class Destination(models.Model):

    name = models.CharField(max_length=100, default="null")
    price = models.IntegerField(default=100)


