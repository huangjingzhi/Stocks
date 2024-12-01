"""
响应数据获取
"""
from datetime import datetime
from django.shortcuts import render, HttpResponse
from django.http import HttpRequest
import os
import sys
import time
import json
os.chdir(sys.path[0])
import pandas as pd

from stock import functions as fs
from stock import DBStock

#LAST_TRANS_DAY = "20221114"

# 每种数据的ID范围都是10
DATA_STOCK_BASE = 1     # 得到当前数据，会计算当天数据
DATA_STOCK_BASE_PRE = 2 # 得到保存的数据
DATA_INDEX_BASE = 11


DATA_STOCK_SLIGHTRISE_DAY = 21
DATA_STOCK_SLIGHTRISE_TRAIN_DAY = 22

DATA_STOCK_BIGRISE_DAY = 31
DATA_STOCK_BIGRISE_TRAIN_DAY = 32

DATA_TYPE_USLESS = 0xfffff


def data_get_stock_base(request):
    assert isinstance(request, HttpRequest)
    ret_dict = {
        "code": 1,
        "msg": "操作成功",
        "data": [
            
            ]
        }
    rq_data = request.GET
    rq_stock = rq_data["stock"]
    if len(rq_stock) == 8:
        rq_stock = rq_stock[:6] + "." + rq_stock[-2:]
    ret_stock_list = []
    df = DBStock.DBStock.stock_get_days(st_name=rq_stock, n_days=120)
    stock_df = df[["trade_date", "open",  "high", "low", "close", "vol"]]
    stock_df["trade_date"] = stock_df["trade_date"].map(fs.time_translate)
    ret_stock_list = stock_df.values.tolist()[::-1]
    ret_dict["data"] = ret_stock_list
    ret = json.dumps(ret_dict)
    
    
    return HttpResponse(ret)

def data_get_stock_base_pre(request):
    assert isinstance(request, HttpRequest)
    ret_dict = {
        "code": 1,
        "msg": "操作成功",
        "data": [
            ]
        }
    ret = json.dumps(ret_dict)
    return HttpResponse(ret)


def data_get_index_base(request):
    assert isinstance(request, HttpRequest)
    ret_dict = {
        "code": 1,
        "msg": "操作成功",
        "data": [
            
            ]
        }
    ret = json.dumps(ret_dict)
    return HttpResponse(ret)

def data_get_stock_slightrise_day():
    pass

def data_get_stock_slightrise_train_day():
    pass

def data_get_stock_bigrise_day():
    pass

def data_get_stock_bigrise_train_day():
    pass

DATA_TYPE_ACTIONS = {
    DATA_STOCK_BASE: data_get_stock_base,
    DATA_STOCK_BASE_PRE: data_get_stock_base_pre,
    DATA_INDEX_BASE: data_get_index_base,

    DATA_STOCK_SLIGHTRISE_DAY: data_get_stock_slightrise_day,
    DATA_STOCK_SLIGHTRISE_TRAIN_DAY:  data_get_stock_slightrise_train_day,

    DATA_STOCK_BIGRISE_DAY: data_get_stock_bigrise_day,
    DATA_STOCK_BIGRISE_TRAIN_DAY: data_get_stock_bigrise_train_day
}


def get_data(request):
    assert isinstance(request, HttpRequest)
    asq = request.GET
    asq_type = DATA_TYPE_USLESS
    if "dtype" in asq.keys():
        asq_type = int(asq["dtype"])
    if asq_type in DATA_TYPE_ACTIONS.keys():
        return DATA_TYPE_ACTIONS[asq_type](request)
    return HttpResponse("ask type no found")
