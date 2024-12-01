
from django.shortcuts import render
from django.shortcuts import render, HttpResponse
from django.http import HttpRequest

import os
import sys
import time
import json
from datetime import datetime

from stock import reqdata
from stock import strategy_rmeanvol
from stock import strategy_box
from stock import strategy_slightrise
from stock import strategy_breakout
from stock import strategy_attend
from stock import DBStock
from stock import strategy_curbreakout
from stock import strategy_volmeanup


def strategy_stock_rmeanvol(request):
    assert isinstance(request, HttpRequest)
    sts = strategy_rmeanvol.StrategyRmeaVol.strategy_rmeanvol_get_target_sts(th=1.5)
    sts = DBStock.DBStock.stock_get_sts_price_drorder(sts)
    sts = sts[:200]
    return render(
       request,
       "SelectList.html",
       {
           "name": "hjz",
           "stocks": sts,
           "dtype": reqdata.DATA_STOCK_BASE
       }
       )
    
def strategy_stock_box(request):
    assert isinstance(request, HttpRequest)
    sts = strategy_box.StrategyBox.strategy_get_sts(strategy_day=180, min_score=1.02, max_score=1.3)
    sts = DBStock.DBStock.stock_get_sts_price_drorder(sts)
    sts = sts[:200]
    return render(
       request,
       "SelectList.html",
       {
           "name": "hjz",
           "stocks": sts,
           "dtype": reqdata.DATA_STOCK_BASE
       }
       )

def strategy_stock_slightrise(request):
    assert isinstance(request, HttpRequest)
    sts = strategy_slightrise.StrategySlightRise.strategy_slightrise_get_target_sts(se_day=3, min_score=0.01, max_socre=0.2)
    sts = DBStock.DBStock.stock_get_sts_price_drorder(sts)
    sts = sts[:200]
    return render(
       request,
       "SelectList.html",
       {
           "name": "hjz",
           "stocks": sts,
           "dtype": reqdata.DATA_STOCK_BASE
       }
       )

def strategy_stock_breakoutvol(request):
    assert isinstance(request, HttpRequest)
    sts = strategy_breakout.StrategyBreakout.strategy_breakout_get_target_sts(min_score=20, max_score=100)
    sts = DBStock.DBStock.stock_get_sts_price_drorder(sts)
    sts = sts[:200]
    return render(
       request,
       "SelectList.html",
       {
           "name": "hjz",
           "stocks": sts,
           "dtype": reqdata.DATA_STOCK_BASE
       }
       )

def strategy_stock_breakoutcmp(request):
    assert isinstance(request, HttpRequest)
    breakout_sts = strategy_breakout.StrategyBreakout.strategy_breakout_get_target_sts(min_score=10, max_score=150)
    box_sts = strategy_box.StrategyBox.strategy_get_sts(strategy_day=180, min_score=0.9, max_score=1.45)
    slightrise_sts = strategy_slightrise.StrategySlightRise.strategy_slightrise_get_target_sts(se_day=3, min_score=-0.1, max_socre=0.4)
    
    sts = list(set(breakout_sts) & set(box_sts) & set(slightrise_sts))
    sts = DBStock.DBStock.stock_get_sts_price_drorder(sts)
    sts = sts[:300]
    return render(
       request,
       "SelectList.html",
       {
           "name": "hjz",
           "stocks": sts,
           "dtype": reqdata.DATA_STOCK_BASE
       }
       )

def strategy_strategy_breakout_volup(request):
    """
    比strategy_stock_breakoutcmp更加严格筛选
    """
    assert isinstance(request, HttpRequest)
    breakout_sts = strategy_breakout.StrategyBreakout.strategy_breakout_get_target_sts(min_score=10, max_score=150)
    box_sts = strategy_box.StrategyBox.strategy_get_sts(strategy_day=180, min_score=0.9, max_score=1.45)
    slightrise_sts = strategy_slightrise.StrategySlightRise.strategy_slightrise_get_target_sts(se_day=3, min_score=0.02, max_socre=0.4)
    volup_sts = strategy_rmeanvol.StrategyRmeaVol.strategy_rmeanvol_get_target_sts(th=1.4)
    sts = list(set(breakout_sts) & set(box_sts) & set(slightrise_sts) & set(volup_sts))
    sts = sts[:]
    sts = DBStock.DBStock.stock_get_sts_price_drorder(sts)
    sts = sts[:300]
    return render(
       request,
       "SelectList.html",
       {
           "name": "hjz",
           "stocks": sts,
           "dtype": reqdata.DATA_STOCK_BASE
       }
       )

def strategy_attend_record_stock(request):
    assert isinstance(request, HttpRequest)
    print(request)
    if request.method == 'POST':
        st_name = request.POST.get('recordstock')
        opt = request.POST.get("opt")
        print(opt)
        print(request.POST.get('recordstock'))
        print(request.POST)
        if opt == '+':
            strategy_attend.StrategyAttendStock.strategy_attend_add_st(st_name=st_name, record_day=DBStock.DBStock.stock_get_curday())
        if opt == '-':
            strategy_attend.StrategyAttendStock.strategy_attend_cancel_st(st_name=st_name)
        return HttpResponse("")
    else:
        return HttpResponse("")
    
def strategy_attend_sts(request):
    assert isinstance(request, HttpRequest)
    sts = strategy_attend.StrategyAttendStock.strategy_attend_get_sts()
    sts = DBStock.DBStock.stock_get_sts_price_drorder(sts)
    sts = sts[:300]
    
    return render(
       request,
       "SelectList.html",
       {
           "name": "hjz",
           "stocks": sts,
           "dtype": reqdata.DATA_STOCK_BASE
       }
       )

def stock_strategy_curbreakout(request):
    assert isinstance(request, HttpRequest)
    sts = strategy_curbreakout.StrategyCurBreakout.get_target_sts()
    sts = DBStock.DBStock.stock_get_sts_price_drorder(sts)
    sts = sts[:300]
    return render(
       request,
       "SelectList.html",
       {
           "name": "hjz",
           "stocks": sts,
           "dtype": reqdata.DATA_STOCK_BASE
       }
       )

def stock_strategy_volmeanup(request):
    assert isinstance(request, HttpRequest)
    last_date = DBStock.DBStock.stock_get_curday()
    volmeanup_sts = strategy_volmeanup.StrategyVolMeanUp.strategy_volmeanup_get_target_sts(last_date, 15, 90, 2, 100)
    box_sts = strategy_box.StrategyBox.strategy_get_sts(strategy_day=180, min_score=0.9, max_score=1.45)
    sts = list(set(volmeanup_sts) & set(box_sts))
    sts = DBStock.DBStock.stock_get_sts_price_drorder(sts)
    sts = sts[:300]
    return render(
       request,
       "SelectList.html",
       {
           "name": "hjz",
           "stocks": sts,
           "dtype": reqdata.DATA_STOCK_BASE
       }
       )