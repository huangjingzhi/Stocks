import time

from stock import DBStock
from stock import stfuns


class StrategyRmeaVol:
    @classmethod
    def strategy_rmeanvol(cls):
        pass
    @classmethod
    def strategy_rmeanvol_task(cls,pre_day=2, after_day=5):
        cls.strategy_rmeanvol_caculate_sts_score_V2(pre_day=pre_day, after_day=after_day)
    @classmethod
    def strategy_rmeanvol_caculate_st_score(cls, st_name, pre_day=2, after_day=5):
        db_name = stfuns.stname_to_dbstandard(st_name=st_name)
        sql_content = '''
                INSERT INTO strategy (trade_date, strategy, stock, score)
                VALUES (
                    (SELECT MAX(trade_date) FROM {}), 
                    'RMEAN_VOL',
                    '{}',
                    (
                        SELECT 
                            CASE 
                                WHEN (
                                    SELECT AVG(vol) FROM (
                                        SELECT 
                                            trade_date, 
                                            vol, 
                                            ROW_NUMBER() OVER (ORDER BY trade_date DESC) AS row_number  
                                        FROM 
                                            {}  
                                        ORDER BY 
                                            trade_date DESC 
                                        LIMIT {}
                                    )
                                ) <> 0 
                                THEN (
                                    SELECT AVG(vol) FROM (
                                        SELECT 
                                            trade_date, 
                                            vol, 
                                            ROW_NUMBER() OVER (ORDER BY trade_date DESC) AS row_number  
                                        FROM 
                                            {}  
                                        ORDER BY 
                                            trade_date DESC 
                                        LIMIT {}
                                    )
                                ) / (
                                    SELECT AVG(vol) FROM (
                                        SELECT 
                                            trade_date, 
                                            vol, 
                                            ROW_NUMBER() OVER (ORDER BY trade_date DESC) AS row_number  
                                        FROM 
                                            {}  
                                        ORDER BY 
                                            trade_date DESC 
                                        LIMIT {}
                                    )
                                )
                                ELSE 1
                            END AS avg_ratio
                    )
                ) ON DUPLICATE KEY UPDATE
                        score = EXCLUDED.score;
                '''.format(db_name, st_name, db_name, after_day+pre_day, db_name, pre_day, db_name, after_day+pre_day)
        DBStock.DBStock.exec_ddL_sql(sql_content=sql_content)
    @classmethod
    def strategy_rmeanvol_caculate_sts_score(cls, pre_day=2, after_day=5):
        sts = DBStock.DBStock.stock_get_allsts()
        for st_name in sts:
            cls.strategy_rmeanvol_caculate_st_score(st_name=st_name, pre_day=pre_day, after_day=after_day)
    @classmethod
    def strategy_rmeanvol_caculate_sts_score_V2(cls, pre_day=2, after_day=5):
        sts = DBStock.DBStock.stock_get_allsts()
        sql_contents = []
        for st_name in sts:
            db_name = stfuns.stname_to_dbstandard(st_name=st_name)
            sql_content = '''
                INSERT INTO strategy (trade_date, strategy, stock, score)
                VALUES (
                    (SELECT MAX(trade_date) FROM {}), 
                    'RMEAN_VOL',
                    '{}',
                    (
                        SELECT 
                            CASE 
                                WHEN (
                                    SELECT AVG(vol) FROM (
                                        SELECT 
                                            trade_date, 
                                            vol, 
                                            ROW_NUMBER() OVER (ORDER BY trade_date DESC) AS row_number  
                                        FROM 
                                            {}  
                                        ORDER BY 
                                            trade_date DESC 
                                        LIMIT {}
                                    )
                                ) <> 0 
                                THEN (
                                    SELECT AVG(vol) FROM (
                                        SELECT 
                                            trade_date, 
                                            vol, 
                                            ROW_NUMBER() OVER (ORDER BY trade_date DESC) AS row_number  
                                        FROM 
                                            {}  
                                        ORDER BY 
                                            trade_date DESC 
                                        LIMIT {}
                                    )
                                ) / (
                                    SELECT AVG(vol) FROM (
                                        SELECT 
                                            trade_date, 
                                            vol, 
                                            ROW_NUMBER() OVER (ORDER BY trade_date DESC) AS row_number  
                                        FROM 
                                            {}  
                                        ORDER BY 
                                            trade_date DESC 
                                        LIMIT {}
                                    )
                                )
                                ELSE 1
                            END AS avg_ratio
                    )
                ) ON DUPLICATE KEY UPDATE
                        score = EXCLUDED.score;
                '''.format(db_name, st_name, db_name, after_day + pre_day, db_name, pre_day, db_name, after_day + pre_day)
            sql_contents.append(sql_content)
        DBStock.DBStock.exec_ddl_sqls(sql_contents=sql_contents)
    @classmethod
    def strategy_rmeanvol_get_target_sts(cls, th=1.5):
        last_day = DBStock.DBStock.stock_get_curday()
        sql_content = '''
            select stock from strategy where strategy='RMEAN_VOL' and trade_date={} and score>{} and substring(stock, 1, 2)!='30' and substring(stock, 1, 2)!='68' and substring(stock, 1, 1)!='8' order by score desc ;
        '''.format(last_day, th)        
        ret_sts = DBStock.DBStock.exec_dml_sql(sql_content=sql_content)
        ret_sts = [x[0] for x in ret_sts]
        return ret_sts