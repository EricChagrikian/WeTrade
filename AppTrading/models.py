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
    amount = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )
    open_price = models.DecimalField(
        max_digits=12,
        decimal_places=10,
        null=True, blank=True
    )###
    close_price = models.DecimalField(
        max_digits=12,
        decimal_places=10,
        blank=True, null=True
    )
    open_datetime = models.DateTimeField(default=datetime.now)
    close_datetime = models.DateTimeField(blank=True, null=True)
    open = models.BooleanField(default=True)
    
