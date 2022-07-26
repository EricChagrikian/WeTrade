from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Trade(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    symbol = models.TextField()
    quantity = models.IntegerField()
    open_price = models.IntegerField()
    close_price = models.IntegerField()
    open_datetime = models.DateTimeField()
    close_datetime = models.DateTimeField()
    open = models.BooleanField()
    
