from .models import Trade
from rest_framework import serializers

class TradeSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Trade
        fields = ('amount','symbol',)

