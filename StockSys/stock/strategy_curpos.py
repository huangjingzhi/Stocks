


import time 
from stock import DBStock
from stock import stfuns

# cmp max 2() and min 2()
# select max(close) as max_val, min(close) as min_val  from (select * from st_000629_sz order by trade_date desc limit 30)

class StrategyCurpos:
    @classmethod
    def strategy_curpos_calcute_sts_score(cls, se_days):
        sts = DBStock.DBStock.stock_get_allsts()
        sql_contents = []
        for st_name in sts:
            tb_name = stfuns.stname_to_dbstandard(st_name=st_name)
            sql_content = '''
                INSERT INTO strategy (trade_date, strategy, stock, score)
                    VALUES (
                        (SELECT MAX(trade_date) FROM {}), 
                        'CURPOS_{}',
                        '{}',
                        (
                            select 
                                case WHEN (max_val - min_val)=0 THEN 1
                                    ELSE (first_val - min_val)/(max_val - min_val) END AS pos
                                    from (select max(close) as max_val, min(close) as min_val, (select close from {} order by trade_date desc limit 1) as first_val  from (select * from {} order by trade_date desc limit {}))
                        )
                    ) ON DUPLICATE KEY UPDATE
                            score = EXCLUDED.score;
            '''.format(tb_name, se_days, st_name, tb_name, tb_name, se_days)
            sql_contents.append(sql_content)
        DBStock.DBStock.exec_ddl_sqls(sql_contents=sql_contents)

"""
select * from strategy where strategy='CURPOS_180' and ((score<0.3 and score>0.01) or score=1) and substr(stock, 1, 2)!='30' and substr(stock, 1, 2)!='68' and substr(stock, 1, 1)!='8' order by score desc;     
"""
    

        