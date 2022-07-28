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

from .serializers import (
    DepositForm,
    WithdrawForm,
)
from .models import Balance


@permission_classes((permissions.AllowAny,))
class BalanceViewSet(viewsets.ViewSet):

    @action(detail=True, methods=['post'])
    def deposit(self, request):

        serializer = DepositForm(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer_instance = Balance.objects.create(
                user=request.user,
                account_balance=request.data["account_balance"], 
                history = datetime.now()
                )


            serializer_instance.save()
            return Response({'status': 'deposit set'})

    @action(detail=True, methods=['post'])
    def withdraw(self, request):

        serializer = WithdrawForm(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer_instance = Balance.objects.create(
                user=request.user,
                account_balance=request.data["account_balance"], 
                history = datetime.now()
                )


            serializer_instance.save()
            return Response({'status': 'deposit set'})
        
    # @action(detail=True, methods=['post'])
    # def deposit(self, request):
    #     queryset = Balance.objects.all()
    #     serializer = DepositForm(queryset)
    #     Balance.account_balance(serializer)
    #     Balance.save()
    #     return Response(serializer.data)
        

    




# class DepositMoneyView(ListView):


#     def form_valid(self, serializer):
#         amount = serializer.cleaned_data.get('amount')
#         account = self.request.user.account
#         now = timezone.now()

#         account.history = now

#         account.Balance.account_balance += amount
#         account.save(
#             update_fields=[
#                 'history',
#                 'account_balance'
#             ]
#         )

#         if request.method == 'POST':
#             serializer = DepositForm(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)        



# @api_view(['POST'])
# class WithdrawMoneyView(request):


#     def form_valid(self, serializer):
#         amount = serializer.cleaned_data.get('amount')
#         account = self.request.user.account
        
#         if not account.withdrawal_date:
#             now = timezone.now()
#             account.withdrawal_date = now

#         account.balance -= form.cleaned_data.get('amount')
#         account.save(
#             update_fields=[
#                 'withdrawal_date',
#                 'balance'
#             ]
#         )

#         messages.success(
#             self.request,
#             f'Successfully withdrawn {amount}$ from your account'
#         )

#         return super().form_valid(form)
