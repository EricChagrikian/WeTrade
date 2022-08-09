from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from yaml import serialize_all
from rest_framework import viewsets, permissions
from requests import request
from rest_framework.decorators import  permission_classes, action
from rest_framework.response import Response
from django.db.models import Q, Max, Sum
from .serializers import TradeSerializers
from .models import Trade
from AppUserBalance.models import Balance
from .crypto import getInfo


@permission_classes((permissions.IsAuthenticated,))
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

            q = Balance.objects.filter(user=request.user)
            max_ids = q.values('user_id').annotate(Max('id')).values_list('id__max')
            balance_before_open=Balance.objects.filter(id__in=max_ids).aggregate(balance=Max('account_balance')).get('balance')
            is_balance_enough = Balance.objects.filter(id__in=max_ids).aggregate(num=Max("account_balance")).get("num")

            if (is_balance_enough >= total and serializer_trade.amount > 0):
                Balance.objects.filter(id__in=max_ids).update(  
                    account_balance=balance_before_open - total
                )                
                serializer_trade.save()
                return Response({'status': 'trade opened'})
            else:
                serializer_trade.delete()
                return Response('Not enough balance for that trade, or the amount user inserted is not higher than 0')


    @action(detail=True, methods=['post'])
    def close(self, request, pk):   
        try:
            opened_trade = Trade.objects.get(user=request.user, id=pk)
        except Trade.DoesNotExist:
            return Response({'status': 'trade not found'})
        
        if not opened_trade.open:
            return Response({'status': 'trade already closed'})
 
        price = getInfo(opened_trade.symbol)

        Trade.objects.update(
            open = False,
            close_price = price,
            close_datetime = timezone.now()
            )

        open_price=Trade.objects.filter(user=request.user, id=pk).aggregate(num=Max("open_price")).get("num")
        closed_price=Trade.objects.filter(user=request.user, id=pk).aggregate(num=Max("close_price")).get("num")
        get_total = float(closed_price - open_price)
        get_quantity = Trade.objects.filter(user=request.user, id=pk).aggregate(num=Max("quantity")).get("num")
        profit_or_loss = get_total*get_quantity
        amount_bought_on_open = Trade.objects.filter(user=request.user, id=pk).aggregate(num=Max("amount")).get("num")  

        q = Balance.objects.filter(user=request.user)
        max_ids = q.values('user_id').annotate(Max('id')).values_list('id__max')
        balance_before_close=Balance.objects.filter(id__in=max_ids).aggregate(balance=Max('account_balance')).get("balance")
        print(balance_before_close)
        Balance.objects.filter(id__in=max_ids).update(  
            account_balance= float(balance_before_close) + profit_or_loss + float(amount_bought_on_open),
            history_balance_update=timezone.now()
        )
        return Response({'status': 'trade closed'})


    @action(detail=True, methods=['get'])
    def list_trades(self, request):
        get_all_trades = Trade.objects.filter(user=request.user).values_list()
        if len(get_all_trades) == 0:
            return Response('Trades listing is empty')
        else:
            return Response(get_all_trades)


    @action(detail=True, methods=['get'])
    def list_opened_trades(self, request):
        get_all_open_trades = Trade.objects.filter(user=request.user, open=1).values_list()
        if len(get_all_open_trades) == 0:
            return Response('No opened trades')
        else:
            return Response(get_all_open_trades)


    @action(detail=True, methods=['get'])
    def list_closed_trades(self, request):
        get_all_closed_trades = Trade.objects.filter(user=request.user, open=0).values_list()
        if len(get_all_closed_trades) == 0:
            return Response('No closed trades')
        else:
            return Response(get_all_closed_trades)


    @action(detail=True, methods=['get'])
    def specific_trade(self, request, pk):
        get_that_trade = Trade.objects.filter(user=request.user, id=pk).values_list()
        if len(get_that_trade) == 0:
            return Response('This trade does not exist')
        else:
            return Response(get_that_trade)

            
    @action(detail=True, methods=['get'])
    def openPNL(self, request):


        is_user_trading=Trade.objects.filter(user=request.user, open=1).values_list()
        if len(is_user_trading) == 0:
            return Response({"No trades to calculate OpenPNL from"})
        
        else:
            is_user_trading_BTC=Trade.objects.filter(user=request.user, open=1, symbol="BTC").values_list()         
            if not len(is_user_trading_BTC) == 0:
                all_open_prices_BTC=Trade.objects.filter(user=request.user, open=1, symbol="BTC").aggregate(num=Sum("open_price")).get("num")
                all__open_quantities_BTC=Trade.objects.filter(user=request.user, open=1, symbol="BTC").aggregate(num=Sum("quantity")).get("num")
                price_current_BTC = getInfo("BTC")

                get_total_amount_when_bought_BTC = float(all__open_quantities_BTC * all_open_prices_BTC)
                get_total_amount_now_BTC = float(all__open_quantities_BTC * price_current_BTC)
                profit_or_loss_BTC=get_total_amount_now_BTC - get_total_amount_when_bought_BTC
            else:
                profit_or_loss_BTC=float(0)

            is_user_trading_ETH=Trade.objects.filter(user=request.user, open=1, symbol="ETH").values_list()         
            if not len(is_user_trading_ETH) == 0:
                all_open_prices_ETH=Trade.objects.filter(user=request.user, open=1, symbol="ETH").aggregate(num=Sum("open_price")).get("num")
                all__open_quantities_ETH=Trade.objects.filter(user=request.user, open=1, symbol="ETH").aggregate(num=Sum("quantity")).get("num")
                price_current_ETH = getInfo("ETH")

                get_total_amount_when_bought_ETH = float(all__open_quantities_ETH * all_open_prices_ETH)
                get_total_amount_now_ETH = float(all__open_quantities_ETH * price_current_ETH)
                profit_or_loss_ETH=get_total_amount_now_ETH - get_total_amount_when_bought_ETH
            else:
                profit_or_loss_ETH=float(0)

            total_profit_or_loss=profit_or_loss_BTC + profit_or_loss_ETH
            return Response({total_profit_or_loss})


    @action(detail=True, methods=['get'])
    def closedPNL(self, request):

        is_user_trading=Trade.objects.filter(user=request.user, open=0).values_list()
        if len(is_user_trading) == 0:
            return Response({"No trades to calculate ClosePNL from"})
        else:
            is_user_trading_BTC=Trade.objects.filter(user=request.user, open=0, symbol="BTC").values_list() 

            if not len(is_user_trading_BTC) == 0:            
                all_closed_prices_BTC=Trade.objects.filter(user=request.user, open=0, symbol="BTC").aggregate(num=Sum("close_price")).get("num")
                all__closed_quantities_BTC=Trade.objects.filter(user=request.user, open=0, symbol="BTC").aggregate(num=Sum("quantity")).get("num")
                price_current_BTC = getInfo("BTC")

                get_total_amount_when_bought_BTC = float(all__closed_quantities_BTC * all_closed_prices_BTC)
                get_total_amount_now_BTC = float(all__closed_quantities_BTC * price_current_BTC)
                profit_or_loss_BTC=get_total_amount_now_BTC - get_total_amount_when_bought_BTC
            else:
                profit_or_loss_BTC=float(0)

            is_user_trading_ETH=Trade.objects.filter(user=request.user, open=0, symbol="ETH").values_list()  
            if not len(is_user_trading_ETH) == 0:               
                all_closed_prices_ETH=Trade.objects.filter(user=request.user, open=0, symbol="ETH").aggregate(num=Sum("close_price")).get("num")
                all__closed_quantities_ETH=Trade.objects.filter(user=request.user, open=0, symbol="ETH").aggregate(num=Sum("quantity")).get("num")
                price_current_ETH = getInfo("ETH")

                get_total_amount_when_bought_ETH = float(all__closed_quantities_ETH * all_closed_prices_ETH)
                get_total_amount_now_ETH = float(all__closed_quantities_ETH * price_current_ETH)
                profit_or_loss_ETH=get_total_amount_now_ETH - get_total_amount_when_bought_ETH
            else:
                profit_or_loss_ETH=float(0)
                
        total_profit_or_loss=profit_or_loss_BTC + profit_or_loss_ETH
        return Response({total_profit_or_loss})


