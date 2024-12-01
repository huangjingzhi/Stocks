
from stock import srcdata_tushare

"""
 nohup python3 task_srctushare_data.py > task_srctushare_data.log 2>&1 &
"""
if __name__=="__main__":
    srcdata_tushare.start_task()