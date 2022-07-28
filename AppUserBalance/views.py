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
            print(all_deposit_amount['deposit'])
            all_withdraw_amount=Balance.objects.filter(user=request.user).aggregate(withdraw=Sum('withdraw_amount'))
            print(all_withdraw_amount['withdraw']   )

            serializer_instance = Balance.objects.create(
                user=request.user,
                deposit_amount=request.data["deposit_amount"], 
                withdraw_amount=0,
                history=datetime.now()
                )

                
            q = Balance.objects.filter(user=request.user)
            max_ids = q.values('user_id').annotate(Max('id')).values_list('id__max')
            print(max_ids)
            Balance.objects.filter(id__in=max_ids).create(  
                account_balance=all_deposit_amount['deposit'] - all_withdraw_amount['withdraw']    
            )
            
            serializer_instance.save()        
            return Response({'status': 'deposit set'}) 

                

    @action(detail=True, methods=['post'])
    def withdraw(self, request):

        serializer = WithdrawForm(data=request.data)
        if serializer.is_valid(raise_exception=True):
            while serializer.is_valid:
                all_deposit_amount=Balance.objects.filter(user=request.user).aggregate(deposit=Sum('deposit_amount'))
                print(all_deposit_amount)
                return all_deposit_amount
            while serializer.is_valid:
                all_withdraw_amount=Balance.objects.filter(user=request.user).aggregate(withdraw=Sum('withdraw_amount'))
                print(all_withdraw_amount)
                return all_withdraw_amount
            

            serializer_instance = Balance.objects.create(                
                user=request.user,
                deposit_amount=0,
                withdraw_amount=request.data["withdraw_amount"], 
                history=datetime.now()       
                )
            add_instance_to_balance = Balance.objects.create(  
                account_balance=all_deposit_amount['deposit'] - all_withdraw_amount['withdraw'] - request.data["withdraw_amount"]    
            )
            
            serializer_instance.save()
            add_instance_to_balance.save()
            
            return Response({'status': 'withdraw set'})
