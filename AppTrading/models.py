from django.db import models
from django.contrib.auth.models import User
from datetime import datetime


# Create your models here.

class Trade(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        )
    symbol = models.TextField()
    amount = models.IntegerField()
    open_price = models.IntegerField(null=True, blank=True)###
    close_price = models.IntegerField(blank=True, null=True)
    open_datetime = models.DateTimeField(default=datetime.now)
    close_datetime = models.DateTimeField(blank=True, null=True)
    open = models.BooleanField(default=True)
    
