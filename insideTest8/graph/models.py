from django.db import models
from portfolio.models import customer_stock_table
# Create your models here.

class stock_table(models.Model):
    stockname = models.CharField(max_length=100, default="null")
    stockname_full = models.CharField(max_length=100, default="null")


