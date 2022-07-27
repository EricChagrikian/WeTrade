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

from .serializers import TradeSerializers
from .models import Trade
from .crypto import getInfo



@permission_classes((permissions.AllowAny,))
class tradeViewSet(viewsets.ViewSet):

    @action(detail=True, methods=['post'])
    def open(self, request):

        serializer = TradeSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            price = getInfo(request.data["symbol"])
            prixtot = price*request.data["quantity"]
            
            return Response(prixtot)
            



