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
from django.db.models import Q, Max

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

            serializer_trade = Trade.objects.create(
                user=request.user,
                amount = total,
                open_price = price,
                symbol = request.data["symbol"],
                quantity = request.data['amount']
                )

            #use the same views as appuserbalance to filter the last existing row only

            q = Balance.objects.filter(user=request.user)
            max_ids = q.values('user_id').annotate(Max('id')).values_list('id__max')
            is_balance_enough = Balance.objects.filter(id__in=max_ids).aggregate(num=Max("account_balance")).get("num")

            if (is_balance_enough >= total):
                serializer_trade.save()
                return Response({'status': 'trade opened'})
            else:
                serializer_trade.delete()
                return Response('Not enough balance for that trade')


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

        open = Trade.objects.filter(user=request.user, id=pk).aggregate(open=Max('open')).get("open")
        if not (open==1):
            opened_trade.delete()
            return Response({'status': 'trade already closed'})

        open_price=Trade.objects.filter(user=request.user, id=pk).aggregate(num=Max("open_price")).get("num")
        get_total = float(price - open_price)
        get_quantity = Trade.objects.filter(user=request.user, id=pk).aggregate(num=Max("quantity")).get("num")
        profit_or_loss = get_total*get_quantity
        print(profit_or_loss)
        amount_bought_on_open = Trade.objects.filter(user=request.user, id=pk).aggregate(num=Max("amount")).get("num")

        balance_before_close=Balance.objects.filter(user=request.user).aggregate(balance=Max('account_balance')).get("balance")
        print(balance_before_close)
        q = Balance.objects.filter(user=request.user)
        max_ids = q.values('user_id').annotate(Max('id')).values_list('id__max')
        Balance.objects.filter(id__in=max_ids).update(  
            account_balance= balance_before_close + profit_or_loss + amount_bought_on_open,
            history_balance_update=timezone.now()
        )


        
        return Response({'status': 'trade closed'})
            



