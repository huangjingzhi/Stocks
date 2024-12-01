from stock import DBStock

class DBStrategy:
    """
    strategy 表相关操作
    """
    @classmethod
    def get_pre_day(cls, pre_n=1):
        sql_content = '''
        select DISTINCT trade_date from strategy order by trade_date desc offset {} limit 1;
        '''.format(pre_n)
        ret = DBStock.DBStock.exec_dml_sql(sql_content=sql_content)
        return ret[0][0]
    @classmethod
    def get_last_day(cls):
        sql_content = '''
            select max(trade_date) from strategy;
        '''
        max_date = DBStock.DBStock.exec_dml_sql(sql_content=sql_content)[0][0]
        return max_date
