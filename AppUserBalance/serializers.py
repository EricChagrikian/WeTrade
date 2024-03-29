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
            'deposit_amount',
        )
        extra_kwargs = {'deposit_amount': {'required': True}}




class WithdrawForm(serializers.ModelSerializer):

    class Meta:
        model = Balance
        fields = (
            'withdraw_amount',
        ) 
        extra_kwargs = {'withdraw_amount': {'required': True}}


