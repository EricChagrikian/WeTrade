from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Cryptocurrency

class CryptocurrencySerializers(serializers.ModelSerializer):
    class Meta:
        model = Cryptocurrency
        fields = ['cryptocurrency', 'price', 'market_cap']