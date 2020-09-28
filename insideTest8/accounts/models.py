from django.db import models
from django.contrib import admin
# Create your models here.

class user_data(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100, default="null")
    last_name = models.CharField(max_length=100, default="null")
    username = models.CharField(max_length=100, default="null")
    email = models.CharField(max_length=100, default="null")

