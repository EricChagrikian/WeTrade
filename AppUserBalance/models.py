from curses import ALL_MOUSE_EVENTS
from optparse import AmbiguousOptionError
from statistics import quantiles
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Balance(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    history = models.DateTimeField(null=True, blank=True)

    history_balance_update = models.DateTimeField(null=True, blank=True)
    
    deposit_amount = models.FloatField(
        default=0
    )
    withdraw_amount = models.FloatField(
        default=0
    )
    account_balance = models.FloatField(
        default=0
    )
    first_balance = models.FloatField(
        default=0
    )