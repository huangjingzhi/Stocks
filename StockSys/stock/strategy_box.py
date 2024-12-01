


import time 
from stock import DBStock
from stock import stfuns

class StrategyBox:
    """
    最近一段时间的最大值/最小值
    """
    @classmethod
    def strategy_box_calcute_sts_score(cls, se_days):
        sts = DBStock.DBStock.stock_get_allsts()
        sql_contents = []
        for st_name in sts:
            tb_name = stfuns.stname_to_dbstandard(st_name=st_name)
            sql_content = '''
                INSERT INTO strategy (trade_date, strategy, stock, score)
                    VALUES (
                        (SELECT MAX(trade_date) FROM {}), 
                        'BOX_{}',
                        '{}',
                        (
                            select max_val/min_val from (select max(close) as max_val, min(close) as min_val  from (select * from {} order by trade_date desc limit {}))
                        )
                    ) ON DUPLICATE KEY UPDATE
                            score = EXCLUDED.score;
            '''.format(tb_name, se_days, st_name, tb_name, se_days)
            sql_contents.append(sql_content)
        DBStock.DBStock.exec_ddl_sqls(sql_contents=sql_contents)
    @classmethod
    def strategy_get_sts(cls, strategy_day=180, min_score=0.5, max_score=1.5):
        last_date = DBStock.DBStock.stock_get_curday()
        sql_content = '''
            select stock from strategy where strategy='BOX_{}' and score>{} and score<{} and trade_date={} and substring(stock, 1, 2)!='30' and substring(stock, 1, 1)!='8' order by score desc ;
        '''.format(strategy_day, min_score, max_score, last_date)
        ret_sts = DBStock.DBStock.exec_dml_sql(sql_content=sql_content)
        ret_sts = [x[0] for x in ret_sts]
        return ret_sts