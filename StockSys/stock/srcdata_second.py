

"""
分钟数据
"""
import urllib.request as req
import pandas as pd
import os
import numpy as np
import time
import requests
import json
from stock import DBStock
from datetime import datetime
from datetime import time as Dtime

def get_url(url):
    res = req.urlopen(url)
    content = res.read()
    content = content.decode("gb2312")
    return content

class SD:
    @classmethod
    def fenshishuju_dfcf(cls, st_code):
        if st_code[-2:] == "SH":
            lsbl = '1.'+st_code[:6]
        else:
            lsbl = '0.' + st_code[:6]   
        
        url_path = "http://push2his.eastmoney.com/api/qt/stock/trends2/get?&fields1=f1%2Cf2%2Cf3%2Cf4%2Cf5%2Cf6%2Cf7%2Cf8%2Cf9" \
                "%2Cf10%2Cf11%2Cf12%2Cf13&fields2=f51%2Cf52%2Cf53%2Cf54%2Cf55%2Cf56%2Cf57%2Cf58&" \
                "ut=7eea3edcaed734bea9cbfc24409ed989&ndays=1&iscr=0&secid=" + lsbl + \
                "&_=1643253749790" + str(time.time)
        resp = requests.get(url_path, timeout=6)
        data = json.loads(resp.text)
        pre_close = data['data']['preClose']
        st_cn_name = data['data']['name']
        ret_data = {'trade_date': [], 'open': [], 'pre_close': [], '均价': [], 'vol': []}
        for k in data['data']['trends']:
            lsbl = k.split(",")
            ret_data['trade_date'].append(lsbl[0].replace('-', '')[:8])
            ret_data['open'].append(eval(lsbl[2]))
            ret_data['pre_close'].append(pre_close)
            ret_data['均价'].append(lsbl[-1])
            ret_data['vol'].append(float(eval(lsbl[-3])))
            
        ret_data = pd.DataFrame(ret_data)
        return ret_data
    @classmethod
    def stock_get_cur_info(cls, stock_name='002277.SZ'):
        """
        当天的基本信息
        """
        df = cls.fenshishuju_dfcf(stock_name)
        ser = df["open"]
        cur_price = df.iloc[-1]["open"]
        max_price = ser.max()
        min_val = ser.min()
        open_val = df.iloc[0]["open"]
        vol_val = df["vol"].sum()
        trade_date = df.iloc[0]['trade_date']
        pre_close = df.iloc[0]['pre_close']
        ret_dict = {
            "trade_date": trade_date,
            "open": open_val,
            "high": max_price,
            "low": min_val,
            "close": cur_price,
            'pre_close': pre_close,
            "vol": vol_val
        }
        return ret_dict
    
    @classmethod
    def sd_st_add_day_data_to_db(cls, st_name):
        st_day_info = cls.stock_get_cur_info(st_name)
        values = [[
            st_day_info['trade_date'],
            st_day_info['open'],
            st_day_info['high'],
            st_day_info['low'],
            st_day_info['close'],
            st_day_info['pre_close'],
            0, # change
            0, # pct_chg
            st_day_info['vol'],
            0  # amount
        ]]
        if not DBStock.DBStock.is_st_db_exits(st_name=st_name):
            DBStock.DBStock.create_stock_table(st_name=st_name)
        DBStock.DBStock.add_stock_days(name=st_name, values=values)
    
    @classmethod
    def sd_update_sts_curday_data(cls):
        sts = DBStock.DBStock.stock_get_allsts()
        for st_name in sts:
            cls.sd_st_add_day_data_to_db(st_name=st_name)
            time.sleep(0.1)
    
    @classmethod
    def sd_is_match_task_time(cls):
        now = datetime.now()
        weekday = now.weekday()
        start_time = Dtime(9, 00)
        end_time = Dtime(15, 30)
        if weekday < 5 and start_time <= now.time() <= end_time:
            return True
        else:
            return False
    
    @classmethod
    def st_update_sts_curday_task(cls):
        while True:
            try:
                if SD.sd_is_match_task_time():
                    SD.sd_update_sts_curday_data()
            except:
                continue
            time.sleep(1)

def start_sd_task():
    print("start second src data!")
    SD.st_update_sts_curday_task()
