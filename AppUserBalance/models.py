from curses import ALL_MOUSE_EVENTS
from optparse import AmbiguousOptionError
from statistics import quantiles
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Balance(models.Model):
    user = models.ForeignKey(
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


    def deposit_total(self, account_balance):
        self.deposit_amount += account_balance
        return account_balance

    def withdraw_total(self, account_balance):
        self.withdraw_amount -= account_balance
        return account_balance



def compute_basic_interest_and_return(basic_deposit_amount):
    basic_interest = basic_deposit_amount * 365 * 0.02/2
    basic_investment_return = basic_deposit_amount + basic_interest

    return (basic_interest, basic_investment_return)

    # def deposit_total(self):
    #     return sum([item.deposit_amount for item in self.items.all()])

    # def withdraw_total(self):
    #     return sum([item.withdraw_amount for item in self.items.all()])

    
    # def save(self, *args, **kwargs):
    #    self.account_balance = self.deposit_total - self.withdraw_total 
    #    super().save(*args, **kwargs)