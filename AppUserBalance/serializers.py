import datetime

from rest_framework import serializers, status
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.conf import settings


from .models import Balance


class DepositForm(serializers.ModelSerializer):

    class Meta:
        model = Balance
        fields = (
            'account_balance',
        )
        extra_kwargs = {'account_balance': {'required': True}}

    # def save(self, commit=True):
    #     self.instance.account_balance = self.account_balance
    #     return super().save()


class WithdrawForm(serializers.ModelSerializer):

    class Meta:
        model = Balance
        fields = [
            'account_balance'
        ]    


    def save(self, commit=True):
        self.instance.account_balance = self.account_balance
        return super().save()

