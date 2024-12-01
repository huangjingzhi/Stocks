

"""
计算3天，5天，10天，20天的比值
"""

import time 
from stock import DBStock
from stock import stfuns

class StrategySlightRise:
    @classmethod
    def strategy_slightrise_calculate_st_score(cls, st_name, se_days=3):
        db_name = stfuns.stname_to_dbstandard(st_name=st_name)
        sql_content = '''
        INSERT INTO strategy (trade_date, strategy, stock, score)
            VALUES (
                (SELECT MAX(trade_date) FROM {}), 
                'SLIGHTRISE_{}',
                '{}',
                (
                     select sum((close/pre_close -1))  from (select close, pre_close from {} order by trade_date desc limit {})
                )
            ) ON DUPLICATE KEY UPDATE
                    score = EXCLUDED.score;
        '''.format(db_name, se_days, st_name, db_name, se_days)
        DBStock.DBStock.exec_ddL_sql(sql_content=sql_content)
    @classmethod
    def strategy_slightrise_calculate_sts_score(cls, se_days):
        sts = DBStock.DBStock.stock_get_allsts()
        sql_contents = []
        for st_name in sts:
            db_name = stfuns.stname_to_dbstandard(st_name=st_name)
            sql_content = '''
            INSERT INTO strategy (trade_date, strategy, stock, score)
                VALUES (
                    (SELECT MAX(trade_date) FROM {}), 
                    'SLIGHTRISE_{}',
                    '{}',
                    (
                        select sum((close / pre_close -1))  from (select close, pre_close from {} order by trade_date desc limit {})
                    )
                ) ON DUPLICATE KEY UPDATE
                        score = EXCLUDED.score;
            '''.format(
                db_name,
                se_days,
                st_name,
                db_name, se_days)
            sql_contents.append(sql_content)
        DBStock.DBStock.exec_ddl_sqls(sql_contents=sql_contents)
    @classmethod
    def strategy_slightrise_get_target_sts(cls, se_day, min_score, max_socre):
        last_date = DBStock.DBStock.stock_get_curday()
        sql_content = '''
            select stock from strategy where strategy='SLIGHTRISE_{}' and score>{} and score<{} and trade_date={}  and substring(stock, 1, 2)!='30' and substring(stock, 1, 1)!='8' order by score desc;
        '''.format(se_day,min_score, max_socre, last_date)
        sts = DBStock.DBStock.exec_dml_sql(sql_content=sql_content)
        return [x[0] for x in sts]