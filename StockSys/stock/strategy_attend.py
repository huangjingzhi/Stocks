
from stock import DBStock



class StrategyAttendStock:
    """
    create table strategy_attendstock (stock text PRIMARY KEY,  first INTEGER, last INTEGER, cnt INTEGER);
    NOTICE:  CREATE TABLE / PRIMARY KEY will create implicit index "strategy_attendstock_pkey" for table "strategy_attendstock"
    create index strategy_attendstock_nameindex on strategy_attendstock(stock);
    """
    @classmethod
    def strategy_attend_add_st(cls, st_name, record_day):
        sql_content = '''
        INSERT INTO strategy_attendstock VALUES ('{}', {}, {}, {}) ON DUPLICATE KEY UPDATE 
            last={},
            cnt=cnt + 1;
        '''.format(st_name, record_day, record_day, 1, record_day)
        DBStock.DBStock.exec_ddL_sql(sql_content=sql_content)
    @classmethod
    def strategy_attend_cancel_st(cls, st_name):
        sql_content = '''
            DELETE FROM strategy_attendstock where stock='{}';
        '''.format(st_name)
        DBStock.DBStock.exec_ddL_sql(sql_content=sql_content)
    @classmethod
    def strategy_attend_get_sts(cls):
        sql_content = '''
            select stock from strategy_attendstock order by last desc;
        '''
        ret = DBStock.DBStock.exec_dml_sql(sql_content=sql_content)
        return [x[0] for x in ret]