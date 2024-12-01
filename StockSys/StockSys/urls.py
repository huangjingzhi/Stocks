"""StockSys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from stock import views as stvs
from stock import reqdata

urlpatterns = [
    path("", stvs.strategy_stock_rmeanvol),
    path("data", reqdata.get_data),
    path('rmeanvol', stvs.strategy_stock_rmeanvol),
    path('box', stvs.strategy_stock_box),
    path('slightrise', stvs.strategy_stock_slightrise),
    path('breakout', stvs.strategy_stock_breakoutvol),
    path('breakoutcmp', stvs.strategy_stock_breakoutcmp),
    path('breakoutvolup', stvs.strategy_strategy_breakout_volup),
    path('recordstock', stvs.strategy_attend_record_stock),
    path('attend', stvs.strategy_attend_sts),
    path('curbeakout', stvs.stock_strategy_curbreakout),
    path('volmeanup', stvs.stock_strategy_volmeanup)
]

