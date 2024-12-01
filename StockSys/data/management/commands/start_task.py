import os
import pandas as pd


data_dir = "../stockdata"

DATA_STOCK_DIR = os.path.join(data_dir, "stock")


# from data.models import Stock

from django.apps import apps
def stock_move_csvdata_to_db(st_path, st_name):
    df = pd.read_csv(st_path)
    # 转为Stock模型的对象并保存
    for index, row in df.iterrows():
        apps.check_apps_ready()
        Stock = apps.get_model('data', 'Stock')
        Stock.add_stock_name(st_name)
        Stock.update_stock(row['trade_date'],
                        row['open'],
                        row['high'],
                        row['low'],
                        row["close"],
                        row["pre_close"],
                        row["change"],
                        row["pct_chg"],
                        row["vol"],
                        row["amount"])

def stock_moveall_csvdata_to_db():
    k = 0
    files = os.listdir(DATA_STOCK_DIR)
    for file in files:
        st_name = file[:-4]
        print(st_name)
        st_path = os.path.join(DATA_STOCK_DIR, file)
        stock_move_csvdata_to_db(st_path=st_path, st_name=st_name)
        k += 1
        if k > 6:
            break

def stock_readdb_stocks():
    apps.check_apps_ready()
    Stock = apps.get_model('data', 'Stock')
    files = os.listdir(DATA_STOCK_DIR)
    for file in files:
        st_name = file[:-4]
        print(st_name)
        df = Stock.get_stock_dataframe("trade_date", 2)
        print(len(df))
        # print(df)
        break
    
    pass


import multiprocessing
from django.core.management.base import BaseCommand

def test():
    print("start_task")
class Command(BaseCommand):
    help = 'Starts a task that runs indefinitely until stopped'

    def handle(self, *args, **options):
        import django
        django.setup()
        # 启动一个子进程执行任务
        p = multiprocessing.Process(target=stock_moveall_csvdata_to_db)
        p = multiprocessing.Process(target=stock_readdb_stocks)
        p.start()
        
        # 将子进程的进程ID存储到一个文件中
        with open('task.pid', 'w') as f:
            f.write(str(p.pid))
