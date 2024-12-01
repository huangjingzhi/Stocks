"""
计算当前一段时间是否出现连续多天量大
"""
from stock import DBStock
from stock import stfuns

class StrategyVolMeanUp:
    """
    create table strategy_volmeanup(trade_date integer, strategy text, stock text, score real, primary key (trade_date, strategy, stock));
    """
    @classmethod
    def strategy_volmeanup_calculate_sts_score(cls, pre_n, after_n):
        sts = DBStock.DBStock.stock_get_allsts()
        sql_contents = []
        
        for st_name in sts:
            db_name = stfuns.stname_to_dbstandard(st_name=st_name)
            sql_content = '''
            INSERT INTO strategy_volmeanup(trade_date, strategy, stock, score)
                VALUES (
                    (SELECT MAX(trade_date) FROM {}), 
                    'strategy_volmeanup_{}_{}',
                    '{}',
                    (
                        case (select avg(t1.vol) as mean_vol2 from (select vol from (select trade_date,vol from {} order by trade_date desc limit {}) t order by t.vol limit {}) t1)
                            when 0 then 0
                            else
                                ((select avg(t1.vol) as mean_vol1 from (select vol from (select trade_date,vol from {} order by trade_date desc limit {}) t order by t.vol limit {}) t1) /
                                (select avg(t1.vol) as mean_vol2 from (select vol from (select trade_date,vol from {} order by trade_date desc limit {}) t order by t.vol limit {}) t1))
                        end
                    )
                ) ON DUPLICATE KEY UPDATE
                        score = EXCLUDED.score;
            '''.format(
                db_name,
                pre_n, after_n,
                st_name,
                db_name, after_n, after_n * 0.6666 ,
                db_name, pre_n, pre_n * 0.6666, 
                db_name, after_n, after_n * 0.6666)
            sql_contents.append(sql_content)
        DBStock.DBStock.exec_ddl_sqls(sql_contents=sql_contents)
    @classmethod
    def strategy_volmeanup_get_target_sts(cls, se_day, pre_n, after_n, min_score, max_socre):
        last_date = DBStock.DBStock.stock_get_curday()
        sql_content = '''
            select stock from strategy_volmeanup  where strategy='strategy_volmeanup_{}_{}' and  score>{} and score<{} and trade_date={}  and substring(stock, 1, 2)!='30' and substring(stock, 1, 1)!='8' order by score desc;
        '''.format(pre_n, after_n, min_score, max_socre, se_day)
        sts = DBStock.DBStock.exec_dml_sql(sql_content=sql_content)
        return [x[0] for x in sts]
    