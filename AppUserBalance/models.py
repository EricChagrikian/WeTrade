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
    
    deposit_amount = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )
    withdraw_amount = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )
    account_balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )