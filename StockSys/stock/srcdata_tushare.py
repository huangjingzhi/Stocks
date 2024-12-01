
# 运行，需要添加token
TOKEN = ""

import tushare as ts
import time
from stock import DBStock
from datetime import datetime
from datetime import time as Dtime

# 初始化数据
ts.set_token(TOKEN)
pro = ts.pro_api()

class TS:
    @classmethod
    def ts_get_sts_day_data(cls, day):
        df =  pro.daily(trade_date=str(day))

        flag = True
        if len(df) <= 0:
            flag = False
        return flag, df
    @classmethod
    def ts_sts_day_data_to_db(cls, day):
        ret_flag, ts_df =  cls.ts_get_sts_day_data(day=day)
        ts_df.set_index('ts_code', inplace=True)
        if ret_flag:
            for st_name, data in ts_df.iterrows():
                values = [[data['trade_date'],
                           data['open'],
                           data['high'],
                           data['low'],
                           data['close'],
                           data['pre_close'],
                           data['change'],
                           data['pct_chg'],
                           data['vol'],
                           data['amount']]]
                if not DBStock.DBStock.is_st_db_exits(st_name=st_name):
                    DBStock.DBStock.create_stock_table(st_name=st_name)
                    
                DBStock.DBStock.add_stock_days(name=st_name, values=values)
    
    @classmethod
    def get_cur_day(cls):
        # 获取当前日期和时间
        current_date = datetime.now()
        # 将日期格式化为yyyymmdd
        formatted_date = int(current_date.strftime('%Y%m%d'))
        return formatted_date
    
    @classmethod
    def is_match_task_time(cls):
        now = datetime.now()
        weekday = now.weekday()
        start_time = Dtime(17, 00)
        end_time = Dtime(18, 00)
        if weekday < 5 and start_time <= now.time() <= end_time:
            return True
        else:
            return False
    
    @classmethod
    def ts_update_sts_day_task(cls):
        while(True):
            try:
                if TS.is_match_task_time():
                    cur_day = TS.get_cur_day()
                    TS.ts_sts_day_data_to_db(cur_day)
            except:
                continue
            time.sleep(10 * 60)

"""
nohup python3 task_srctushare_data.py > task_srctushare_data.log 2>&1 &
"""
def start_task():
    print("start srcdata_tushare")
    TS.ts_update_sts_day_task()
    