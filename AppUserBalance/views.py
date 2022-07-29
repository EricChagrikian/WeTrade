from datetime import datetime
from django.shortcuts import render

# Create your views here.

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView
from yaml import serialize_all
from rest_framework import viewsets, permissions
from requests import request
from rest_framework.decorators import api_view, permission_classes, action
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
                    
                q = Balance.objects.filter(user=request.user)
                max_ids = q.values('user_id').annotate(Max('id')).values_list('id__max')
                Balance.objects.filter(id__in=max_ids).update(  
                    account_balance=all_deposit_amount['deposit'] - all_withdraw_amount['withdraw'] + request.data["deposit_amount"]
                )
                return Response({'status': 'deposit set'}) 
            else:
                serializer_instance.delete()
                return Response({'Value has to be above 0'})
            # is_first_update = Balance.objects.filter(id__in=max_ids).values('history_balance_update')
            # print(is_first_update)
            # if (is_first_update == None):
            #     return Response({'status': 'deposit set'}) 
            # else:
            #     Balance.objects.filter(id__in=max_ids).update(history_balance_update=timezone.now())
            #     return Response({'status': 'deposit set'}) 

    @action(detail=True, methods=['get'])
    def check_balance(self, request):  
        current_balance=Balance.objects.filter(user=request.user).aggregate(balance=Max('account_balance')).get("balance")
        print(current_balance)
        if not current_balance:
            return Response({'0 credits'}) 
        return Response({current_balance + ' credits'}) 
    

    @action(detail=True, methods=['post'])
    def withdraw(self, request):

        serializer = WithdrawForm(data=request.data)
        if serializer.is_valid(raise_exception=True):

            all_deposit_amount=Balance.objects.filter(user=request.user).aggregate(deposit=Sum('deposit_amount'))
            all_withdraw_amount=Balance.objects.filter(user=request.user).aggregate(withdraw=Sum('withdraw_amount'))
            

            serializer_instance = Balance.objects.create(                
                user=request.user,
                deposit_amount=0,
                withdraw_amount=request.data["withdraw_amount"], 
                history=timezone.now()       
                )

            if (serializer_instance.withdraw_amount > 0):
                serializer_instance.save()
            
                q = Balance.objects.filter(user=request.user)
                max_ids = q.values('user_id').annotate(Max('id')).values_list('id__max')
                Balance.objects.filter(id__in=max_ids).update(  
                    account_balance=all_deposit_amount['deposit'] - all_withdraw_amount['withdraw'] - request.data["withdraw_amount"],
                    history_balance_update=timezone.now()
                )
                return Response({'status': 'withdraw set'})
            else:
                serializer_instance.delete()
                return Response({'Value has to be above 0'})
