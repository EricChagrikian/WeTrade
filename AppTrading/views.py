from datetime import datetime
from decimal import Decimal
from django.shortcuts import render

# Create your views here.

from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView
from yaml import serialize_all
from rest_framework import viewsets, permissions
from requests import request
from rest_framework.decorators import  permission_classes, action
from rest_framework.response import Response
from django.db.models import Q

from .serializers import TradeSerializers
from .models import Trade
from AppUserBalance.models import Balance
from .crypto import getInfo



@permission_classes((permissions.AllowAny,))
class tradeViewSet(viewsets.ViewSet):

    @action(detail=True, methods=['post'])
    def open(self, request):

        serializer = TradeSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            price = getInfo(request.data["symbol"])
            
            total = price * request.data['amount']


            #use the same views as appuserbalance to filter the last existing row only
            is_balance_enough = Balance.objects.filter(user=request.user).values_list('account_balance')
            print(is_balance_enough)

            serializer_trade = Trade.objects.create(
                user=request.user,
                amount = total,
                open_price = price,
                symbol = request.data["symbol"],
                )
            
            serializer_trade.save()
            return Response({'status': 'trade opened'})

    @action(detail=True, methods=['post'])
    def close(self, request, pk):
        try:
            opened_trade = Trade.objects.get(user=request.user, id=pk)
        except Trade.DoesNotExist:
            return Response({'status': 'trade not found'})
        
        if not opened_trade.open:
            return Response({'status': 'trade already closed'})
 
        price = getInfo(opened_trade.symbol)
        opened_trade.close_price = price
        opened_trade.close_datetime = timezone.now()
        opened_trade.open = False
        opened_trade.save()

        print(request)
        
        return Response({'status': 'trade closed'})
            



