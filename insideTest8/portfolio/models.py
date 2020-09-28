from django.db import models

# Create your models here.
#from accounts.models import user_data
from django.contrib.auth.models import User,auth



class portfoliodata(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    stockname = models.CharField(max_length=100, default="null")
    quantity = models.IntegerField(default=100)
    current_quantity = models.IntegerField(default=0)
    dateofpurchase = models.DateField()
    transaction = models.CharField(max_length=100, default="null")

class customer_stock_table(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    stockname = models.CharField(max_length=100, default="null")
    quantity = models.IntegerField(default=100)

