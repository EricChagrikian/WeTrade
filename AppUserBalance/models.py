from curses import ALL_MOUSE_EVENTS
from optparse import AmbiguousOptionError
from statistics import quantiles
from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Balance(models.Model):
    user = models.OneToOneField(
        User,
        related_name='account',
        on_delete=models.CASCADE,
    )
    account_balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )
    history = models.DateTimeField(null=True, blank=True)

