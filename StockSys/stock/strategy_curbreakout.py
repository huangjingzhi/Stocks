from stock import DBStrategy
from stock import DBStock
from stock import strategy_breakout
from stock import stfuns

class StrategyCurBreakout:
    @classmethod
    def get_target_sts(cls, min_th=1, max_th=1.2):
        last_date = DBStock.DBStock.stock_get_curday()
        pre_day = DBStrategy.DBStrategy.get_pre_day(pre_n=2)
        sql_content = '''
            select stock from strategy where trade_date={} and strategy='BOX_30' and score>={} and score <={} and substring(stock, 1, 2)!='30' and substring(stock, 1, 3)!='688' and substring(stock, 1, 1)!='8';
        '''.format(pre_day, min_th, max_th)
        pre_box_sts = DBStock.DBStock.exec_dml_sql(sql_content=sql_content)
        pre_box_sts = [x[0] for x in pre_box_sts]
        sql_content = '''
            select stock from strategy where  trade_date={} and strategy='RMEAN_VOL' and score>=1.3 and substring(stock, 1, 2)!='30' and substring(stock, 1, 3)!='688' and substring(stock, 1, 1)!='8' order by trade_date desc; 
        '''.format(last_date)
        pre_rmean_vol_sts = DBStock.DBStock.exec_dml_sql(sql_content=sql_content)
        pre_rmean_vol_sts = [x[0] for x in pre_rmean_vol_sts]
        
        breakout_sts = strategy_breakout.StrategyBreakout.strategy_breakout_get_target_sts(min_score=10, max_score=100)
        
        breakout_price_sts = cls.strategy_curbeakout_price_get_target_sts(trade_date=last_date, min_th=2, max_th=10)
        
        sts = list(set(pre_box_sts) & (set(pre_rmean_vol_sts)|set(breakout_price_sts)) & set(breakout_sts))
        return  sts
    @classmethod
    def strategy_curbeakout_price_calculate_sts(cls, pre_n=3, af_n=10):
        """
        计算最近的price 变化相比
        """
        sts = DBStock.DBStock.stock_get_allsts()
        sql_contents = []
        for st_name in sts:
            db_name = stfuns.stname_to_dbstandard(st_name=st_name)
            sql_content = '''
                INSERT INTO strategy (trade_date, strategy, stock, score)
                VALUES (
                    (SELECT MAX(trade_date) FROM {}), 
                    'CURBREAKOUT_PRICE',
                    '{}',
                    (
                        select (
                            (select max(dr) from (select abs(close/pre_close -1) as dr from {} order by trade_date desc offset 0 limit {}))
                            /
                            (select max(dr) from (select (abs(close/pre_close -1)) as dr from {} order by trade_date desc offset {} limit {}))
                        
                        ) as score
                        
                    )
                ) ON DUPLICATE KEY UPDATE
                        score = EXCLUDED.score;
            '''.format(db_name, st_name, db_name, pre_n, db_name, pre_n, af_n)
            sql_contents.append(sql_content)
        DBStock.DBStock.exec_ddl_sqls(sql_contents=sql_contents)
    @classmethod
    def strategy_curbeakout_price_get_target_sts(cls,trade_date=20231027, min_th=2, max_th=10):
        sql_content = '''
            select stock from strategy where strategy='CURBREAKOUT_PRICE' and trade_date={} and score>={}  and score<={} and substring(stock, 1, 2)!='30' and substring(stock, 1, 3)!='688' and substring(stock, 1, 1)!='8';
        '''.format(trade_date,min_th, max_th)
        sts = DBStock.DBStock.exec_dml_sql(sql_content=sql_content)
        return [x[0] for x in sts]
    @classmethod
    def strategy_curbeakout_change_calculate_sts(cls, pre_n=3, af_n=10):
        """
        暂时没有换手率的数据
        """
        pass
    @classmethod
    def trategy_curbreakout_task(cls):
        cls.strategy_curbeakout_price_calculate_sts()
        