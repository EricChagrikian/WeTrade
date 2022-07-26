from django.shortcuts import render
from rest_framework import generics
from .models import Cryptocurrency
from .serializers import CryptocurrencySerializers

# Create your views here.

class ListCryptocurrencyView(generics.ListAPIView):
    queryset = Cryptocurrency.objects.all()
    serializer_class = CryptocurrencySerializers
