from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils import timezone
from yaml import serialize_all
from rest_framework import viewsets, permissions
from requests import request
from rest_framework.decorators import permission_classes, action
from rest_framework.response import Response
from django.db.models import Sum, Max
import numbers
from .serializers import (
    DepositForm,
    WithdrawForm,
)
from .models import Balance


@permission_classes((permissions.IsAuthenticated,))
class BalanceViewSet(viewsets.ViewSet):
 
    @action(detail=True, methods=['post'])
    def deposit(self, request):  

        serializer = DepositForm(data=request.data)
        if serializer.is_valid(raise_exception=True):

            all_deposit_amount=Balance.objects.filter(user=request.user).aggregate(deposit=Sum('deposit_amount'))
            all_withdraw_amount=Balance.objects.filter(user=request.user).aggregate(withdraw=Sum('withdraw_amount'))

            serializer_instance = Balance.objects.create(
                user=request.user,
                deposit_amount=request.data["deposit_amount"], 
                withdraw_amount=0,
                history=timezone.now()
                )
            if (serializer_instance.deposit_amount > 0):     
                serializer_instance.save() 

            if (serializer_instance.deposit_amount > 0):      
                q = Balance.objects.filter(user=request.user)
                max_ids = q.values('user_id').annotate(Max('id')).values_list('id__max')

                get_all_deposits=all_deposit_amount['deposit']
                get_all_withdraw=all_withdraw_amount['withdraw']
                if get_all_deposits==None:
                    get_all_deposits=0

                Balance.objects.filter(id__in=max_ids).update(  
                    account_balance=get_all_deposits - get_all_withdraw + request.data["deposit_amount"]
                )
                
                return Response({'status': 'deposit set'}) 
            else:
                serializer_instance.delete()
                return Response({'Value has to be above 0'})
                

    @action(detail=True, methods=['get'])
    def check_balance(self, request):  
        q = Balance.objects.filter(user=request.user)
        max_ids = q.values('user_id').annotate(Max('id')).values_list('id__max')
        current_balance=Balance.objects.filter(id__in=max_ids).aggregate(balance=Max('account_balance')).get("balance")
        if not current_balance:
            return Response('0 credits') 
        else:   
            return Response(current_balance) 


    @action(detail=True, methods=['post'])
    def withdraw(self, request):

        serializer = WithdrawForm(data=request.data)
        if serializer.is_valid(raise_exception=True):

            all_deposit_amount=Balance.objects.filter(user=request.user).aggregate(deposit=Sum('deposit_amount'))
            all_withdraw_amount=Balance.objects.filter(user=request.user).aggregate(withdraw=Sum('withdraw_amount'))
            

            serializer_instance = Balance.objects.create(                
                user=request.user,
                deposit_amount=0,
                withdraw_amount=float(request.data["withdraw_amount"]), 
                history=timezone.now()       
                )

            q = Balance.objects.filter(user=request.user)
            max_ids = q.values('user_id').annotate(Max('id')).values_list('id__max') 

            balance_before_withdraw=Balance.objects.filter(id__in=max_ids).aggregate(balance=Max('account_balance')).get("balance")
            
            if (float(serializer_instance.withdraw_amount) > 0 and float(serializer_instance.withdraw_amount) < balance_before_withdraw):
                serializer_instance.save()
            
                Balance.objects.filter(id__in=max_ids).update(  
                    account_balance=float(all_deposit_amount['deposit']) - float(all_withdraw_amount['withdraw']) - float(request.data["withdraw_amount"]),
                    history_balance_update=timezone.now()
                )
                return Response({'status': 'withdraw set'})
            else:
                serializer_instance.delete()
                return Response({'Value has to be above 0 and not exceed your current balance'})
