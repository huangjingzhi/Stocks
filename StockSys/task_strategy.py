from datetime import datetime
from datetime import time as Dtime
import time as t

from stock import strategy_box
from stock import strategy_breakout
from stock import strategy_breakoutlow
from stock import strategy_curpos
from stock import strategy_keepvolup
from stock import strategy_rmeanpriceup
from stock import strategy_rmeanvol
from stock import strategy_slightrise
from stock import strategy_curbreakout
from stock import strategy_volmeanup


class StrategyTask:
    @classmethod
    def strategy_task(cls):
        strategy_box.StrategyBox.strategy_box_calcute_sts_score(se_days=30)
        strategy_box.StrategyBox.strategy_box_calcute_sts_score(se_days=50)
        strategy_box.StrategyBox.strategy_box_calcute_sts_score(se_days=120)
        strategy_box.StrategyBox.strategy_box_calcute_sts_score(se_days=180)
        
        strategy_breakout.StrategyBreakout.strategy_breakout_calcute_sts_score_V2()

        strategy_curpos.StrategyCurpos.strategy_curpos_calcute_sts_score(se_days=30)
        strategy_curpos.StrategyCurpos.strategy_curpos_calcute_sts_score(se_days=50)
        strategy_curpos.StrategyCurpos.strategy_curpos_calcute_sts_score(se_days=120)
        strategy_curpos.StrategyCurpos.strategy_curpos_calcute_sts_score(se_days=180)

        strategy_rmeanvol.StrategyRmeaVol.strategy_rmeanvol_task(pre_day=2, after_day=5)
        
        strategy_slightrise.StrategySlightRise.strategy_slightrise_calculate_sts_score(se_days=3)
        strategy_slightrise.StrategySlightRise.strategy_slightrise_calculate_sts_score(se_days=5)
        strategy_curbreakout.StrategyCurBreakout.trategy_curbreakout_task()

        strategy_volmeanup.StrategyVolMeanUp.strategy_volmeanup_calculate_sts_score(15, 90)
        strategy_volmeanup.StrategyVolMeanUp.strategy_volmeanup_calculate_sts_score(15, 60)
        strategy_volmeanup.StrategyVolMeanUp.strategy_volmeanup_calculate_sts_score(30, 120)

    @classmethod
    def task(cls):
        cls.strategy_task()
        while True:
            t.sleep(5 * 60)
            if cls.is_match_task_time():
                try:
                    cls.strategy_task()
                except:
                    continue
        
    @classmethod
    def is_match_task_time(cls):
        now = datetime.now()
        weekday = now.weekday()
        start_time = Dtime(18, 30)
        end_time = Dtime(19, 0)
        if weekday < 5 and start_time <= now.time() <= end_time:
            return True
        else:
            return False
"""
 nohup python3 task_strategy.py > task_strategy.log 2>&1 &
"""
if __name__=="__main__":
    StrategyTask.task()
