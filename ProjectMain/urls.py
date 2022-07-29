"""ProjectMain URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from AppRegister.views import *
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from AppRegister.views import MyObtainTokenPairView
from rest_framework_simplejwt.views import TokenRefreshView
from AppUserBalance import views
from AppTrading.views import tradeViewSet



urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/api-auth/', include('rest_framework.urls')),
    path('api/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/',RegisterUserAPIView.as_view()),
    # path('api/profile/',UserViewSet.as_view({'get': 'queryset'})),    
    path('api/login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('api/login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/balance/', views.BalanceViewSet.as_view({'get': 'check_balance'})), #view current balance
    path('api/balance/deposit/', views.BalanceViewSet.as_view({'post': 'deposit'})), #deposit money from balance
    path('api/balance/withdraw/', views.BalanceViewSet.as_view({'post': 'withdraw'})), #withdraw money from balance
    path('api/trade/index',tradeViewSet.as_view({'get': 'list_trades'})), #list of all the trades of the authenticated user with details
    path('api/trade/<int:pk>',tradeViewSet.as_view({'get': 'specific_trade'})), #details of one specific trade
    path('api/trade/openPNL/',tradeViewSet.as_view({'get': 'openPNL'})), #shows profit or loss of all open trades
    path('api/trade/closePNL/',tradeViewSet.as_view({'get': 'closedPNL'})), #shows profit or loss of all closed trades
    path('api/trade/open',tradeViewSet.as_view({'get': 'list_opened_trades'})), #lists opened trades details of authenticated user
    path('api/trade/close',tradeViewSet.as_view({'get': 'list_closed_trades'})), #lists closed trades details of authenticated user
    path('api/trade/open',tradeViewSet.as_view({'post': 'open'})),
    path('api/trade/close/<int:pk>',tradeViewSet.as_view({'post': 'close'})),
]

router = DefaultRouter()
router.register('user', UserViewSet, basename='user')

urlpatterns += router.urls