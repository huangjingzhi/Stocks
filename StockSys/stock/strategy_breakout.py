
import time 
from stock import DBStock
from stock import stfuns

# CREATE TABLE strategy (
#     trade_date INTEGER,
#     strategy TEXT,
#     stock TEXT,
#     score DOUBLE PRECISION,
#     PRIMARY KEY (trade_date, strategy, stock)
# );
# select * from strategy;

class StrategyBreakout:
    @classmethod
    def strategy_breakout_calcute_st_score(cls, st_name, pre_day=3, after_day=5, th_dr=3, total_day=120):
        """
        """
        tb_name = stfuns.stname_to_dbstandard(st_name=st_name)
        sql_content = '''
        INSERT INTO strategy (trade_date, strategy, stock, score)
            SELECT 
                MAX(trade_date),
                'BREAKOUT_VOL',
                '{}',
                SUM(CASE WHEN mean_dr > {} THEN mean_dr ELSE 0 END)
            FROM 
                (
                SELECT 
                    trade_date,
                    AVG(vol) OVER (ORDER BY trade_date ROWS BETWEEN {} PRECEDING AND 0 FOLLOWING) /
                    AVG(lag_vol_3) OVER (ORDER BY trade_date ROWS BETWEEN {} PRECEDING AND 0 FOLLOWING) AS mean_dr
                FROM 
                    (
                    SELECT 
                        trade_date,
                        vol,
                        LAG(vol, {}) OVER (ORDER BY trade_date) AS lag_vol_3
                    FROM 
                        {}
                    ORDER BY 
                        trade_date DESC
                    LIMIT {}
                    ) AS windowed_data
                ) AS subquery
        ON DUPLICATE KEY UPDATE
                score = EXCLUDED.score;
        '''.format(st_name, th_dr, pre_day - 1, after_day - 1, pre_day, tb_name, total_day)
        DBStock.DBStock.exec_ddL_sql(sql_content=sql_content)
    @classmethod
    def strategy_breakout_calcute_sts_score(cls):
        sts = DBStock.DBStock.stock_get_allsts()
        for st in sts:
            cls.strategy_breakout_calcute_st_score(st_name=st)
    @classmethod
    def strategy_breakout_calcute_sts_score_V2(cls, pre_day=3, after_day=5, th_dr=3, total_day=120):
        sts = DBStock.DBStock.stock_get_allsts()
        sql_contents = []
        for st_name in sts:
            tb_name = stfuns.stname_to_dbstandard(st_name=st_name)
            sql_content = '''
            INSERT INTO strategy (trade_date, strategy, stock, score)
                SELECT 
                    MAX(trade_date),
                    'BREAKOUT_VOL',
                    '{}',
                    SUM(CASE WHEN mean_dr > {} THEN mean_dr ELSE 0 END)
                FROM 
                    (
                    SELECT 
                        trade_date,
                        (AVG(vol) OVER (ORDER BY trade_date ROWS BETWEEN {} PRECEDING AND 0 FOLLOWING) + 0.0001) /
                        (0.0001 + AVG(lag_vol_3) OVER (ORDER BY trade_date ROWS BETWEEN {} PRECEDING AND 0 FOLLOWING)) AS mean_dr
                    FROM 
                        (
                        SELECT 
                            trade_date,
                            vol,
                            LAG(vol, {}) OVER (ORDER BY trade_date) AS lag_vol_3
                        FROM 
                            {}
                        ORDER BY 
                            trade_date DESC
                        LIMIT {}
                        ) AS windowed_data
                    ) AS subquery
            ON DUPLICATE KEY UPDATE
                    score = EXCLUDED.score;
            '''.format(st_name, th_dr, pre_day - 1, after_day - 1, pre_day, tb_name, total_day)
            sql_contents.append(sql_content)
        DBStock.DBStock.exec_ddl_sqls(sql_contents=sql_contents)
    @classmethod
    def strategy_breakout_get_target_sts(cls, max_score, min_score):
        last_day = DBStock.DBStock.stock_get_curday()
        sql_content = '''
            select stock from strategy where strategy='BREAKOUT_VOL' and trade_date={} and score>{} and score<={} and substring(stock, 1, 2)!='30' and substring(stock, 1, 2)!='68' and substring(stock, 1, 1)!='8' order by score desc ;
        '''.format(last_day, min_score, max_score)
        
        target_sts = DBStock.DBStock.exec_dml_sql(sql_content=sql_content)
        return [x[0] for x in target_sts]