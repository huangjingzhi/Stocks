
# -*- coding: utf-8 -*-

import os
import psycopg2
from psycopg2 import pool
from stock import stfuns
import pandas as pd

# 处理float类型的数据函数，保留3位小数
def process_float_round2(value):
    if isinstance(value, float):
        return round(value, 2)
    return value
def process_float_round3(value):
    if isinstance(value, float):
        return round(value, 3)
    return value
class DBStock:
    db_pool = None
    @classmethod
    def init_db_pool(cls, db_host, db_user, db_pwd, db_port, db_name, max_connect=20):
        cls.db_pool = pool.ThreadedConnectionPool(minconn=2, maxconn=max_connect,
                                              host=db_host,
                                              user=db_user,
                                              database=db_name,
                                              password=db_pwd,
                                              port=db_port)
    @classmethod
    def destroy_pool(cls):
        cls.db_pool.closeall()
    
    @classmethod
    def exec_ddL_sql(cls, sql_content):
        cnn = cls.db_pool.getconn()
        try:
            cursor = cnn.cursor()
            cursor.execute(sql_content)
            cnn.commit() 
            # 释放连接回连接池
            cursor.close()
        finally:
            cls.db_pool.putconn(cnn)
    @classmethod
    def exec_ddl_sqls(cls, sql_contents=[]):
        """
        执行多条sql语句
        """
        cnn = cls.db_pool.getconn()
        try:
            cursor = cnn.cursor()
            for sql_content in sql_contents:
                cursor.execute(sql_content)
            cnn.commit() 
            # 释放连接回连接池
            cursor.close()
        finally:
            cls.db_pool.putconn(cnn)
    @classmethod
    def exec_dml_sql(cls, sql_content):
        cnn = cls.db_pool.getconn()
        try:
            cursor = cnn.cursor()
            cursor.execute(sql_content)
            data = cursor.fetchall()
            cnn.commit() 
            # 释放连接回连接池
            cursor.close()
        finally:
            cls.db_pool.putconn(cnn)
        return data
    @classmethod
    def exec_stock_df_days(cls, st_name, n_days=180, dtypes={'trade_date': int,
                                                'open'      : float,
                                                'high'      : float,
                                                'low'       : float,
                                                'close'     : float,
                                                'pre_close' : float,
                                                'change'    : float,
                                                'pct_chg'   : float,
                                                'vol'       : float,
                                                'amount'    : float}):
        st_db_name = stfuns.stname_to_dbstandard(st_name=st_name)
        cnn = cls.db_pool.getconn()
        try:
            df = pd.read_sql_query(f"SELECT * FROM {st_db_name} ORDER BY trade_date DESC LIMIT {n_days}", con=cnn, dtype=dtypes)
        finally:
            cls.db_pool.putconn(cnn)
        return df
    @classmethod
    def add_stock_day(cls, name, trade_date, open, high, low, close,pre_close,change,pct_chg,vol,amount):
        values = [(trade_date, open, high, low, close, pre_close, change, pct_chg, vol, amount)]
        cls.add_stock_days(name=name, values=values)
    @classmethod
    def add_stock_days(cls, name, values):
        """
        INSERT INTO table_name (key_column, other_columns)
            VALUES (value1, value2, ...), (value1, value2, ...)
            ON CONFLICT (key_column) DO UPDATE SET
            other_column = EXCLUDED.other_column;
        """
        tb_name = stfuns.stname_to_dbstandard(name)
        cnn = cls.db_pool.getconn()
        try:
            cursor = cnn.cursor()
            sql_statement = '''INSERT INTO {} 
                            (trade_date, open, high, low, close, pre_close, change, pct_chg, vol, amount) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)  ON DUPLICATE KEY UPDATE        
                                    open = EXCLUDED.open,
                                    high = EXCLUDED.high,
                                    low = EXCLUDED.low,
                                    close = EXCLUDED.close,
                                    pre_close = EXCLUDED.pre_close,
                                    change = EXCLUDED.change,
                                    pct_chg = EXCLUDED.pct_chg,
                                    vol = EXCLUDED.vol,
                                    amount = EXCLUDED.amount;'''.format(tb_name)
            cursor.executemany(sql_statement, values)
            cnn.commit() 
            # 释放连接回连接池
            cursor.close()
        finally:
            cls.db_pool.putconn(cnn)
    @classmethod
    def create_stock_table(cls, st_name):
        """
        """
        st_db_name = stfuns.stname_to_dbstandard(st_name=st_name)
        sql_content = '''CREATE TABLE IF NOT EXISTS {} 
                            (trade_date INTEGER PRIMARY KEY, 
                                open REAL, 
                                high REAL, 
                                low REAL, 
                                close REAL, 
                                pre_close REAL, 
                                change REAL, 
                                pct_chg REAL, 
                                vol REAL, 
                                amount REAL);'''.format(st_db_name)
        cls.exec_ddL_sql(sql_content=sql_content)
        sql_content = "CREATE UNIQUE INDEX  IF NOT EXISTS {} ON {}(trade_date);".format(st_db_name + "_index", st_db_name)
        cls.exec_ddL_sql(sql_content=sql_content)
    @classmethod
    def stock_csv_to_db(cls, st_name, file_path, dtypes={'trade_date': int},
                                                converters={
                                                        'open'      : process_float_round2,
                                                        'high'      : process_float_round2,
                                                        'low'       : process_float_round2,
                                                        'close'     : process_float_round2,
                                                        'pre_close' : process_float_round2,
                                                        'change'    : process_float_round2,
                                                        'pct_chg'   : process_float_round2,
                                                        'vol'       : process_float_round2,
                                                        'amount'    : process_float_round3}):
        """
        trade_date open   high    low  close  pre_close  change  pct_chg         vol       amount  trade_date
        数据转换可以通过dtypes或者和converteers转换
        """
        df = pd.read_csv(file_path, dtype=dtypes, converters=converters)
        values = df.values
        if not cls.is_st_db_exits(st_name=st_name):
            cls.create_stock_table(st_name=st_name)
        cls.add_stock_days(st_name, values)
    @classmethod
    def stock_csvdir_to_db(cls, dir='/home/perf/projects/opengauss/stock/stock'):
        """
        将目录下的所有数据导入数据库中
        """
        files = os.listdir(dir)
        file_number = len(files)
        k = 1
        for file in files:
            file_path = os.path.join(dir, file)
            st_name = file[:-4]
            print("{}/{}: {}_{}".format(k, file_number, st_name, file_path))
            cls.stock_csv_to_db(st_name=st_name, file_path=file_path)
            k += 1
            
    
    @classmethod
    def stock_get_days(cls, st_name , n_days):
        """
        获取最近几天数据
        """
        
        st_db_name = stfuns.stname_to_dbstandard(st_name=st_name)
        sql_content = f"SELECT * FROM {st_db_name} ORDER BY trade_date DESC LIMIT {n_days}"
        start_t = time.time()
        data = cls.exec_dml_sql(sql_content)
        
        start_t = time.time()
        df = pd.DataFrame(data, columns=['trade_date', 'open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg', 'vol', 'amount'])        
        return df
    @classmethod
    def is_st_db_exits(cls, st_name):
        st_db_name = stfuns.stname_to_dbstandard(st_name=st_name)
        sql_content = "SELECT tablename FROM pg_tables WHERE schemaname='{}' and tablename='{}';".format('omm', st_db_name)
        ret = cls.exec_dml_sql(sql_content=sql_content)
        return len(ret) >= 1

    @classmethod
    def stock_get_allsts(cls):
        sql_content = "select tablename from pg_tables where schemaname='omm' and tablename ~ '^st_[0-9]{6}_[a-zA-Z]{2}$'"
        sts = cls.exec_dml_sql(sql_content=sql_content)
        sts_name = [ stfuns.st_dbname_to_stname(x[0]) for x in sts]
        
        return sts_name
    @classmethod
    def stock_get_curday(cls):
        sql_content = '''
            select max(trade_date) from strategy;
        '''
        max_date = cls.exec_dml_sql(sql_content=sql_content)[0][0]
        return max_date
    @classmethod
    def stock_get_st_price_dr(cls, st_name):
        db_name = stfuns.stname_to_dbstandard(st_name=st_name)
        sql_content = '''
            select (close - pre_close)/pre_close from {} order by trade_date desc limit 1;
        '''.format(db_name)
        ret = cls.exec_dml_sql(sql_content=sql_content)
        return float(ret[0][0])
    @classmethod
    def stock_get_sts_price_drorder(cls, st_names):
        rets = dict()
        for st_name in st_names:
            rets[st_name] = cls.stock_get_st_price_dr(st_name=st_name)
        sorted_dict = dict(sorted(rets.items(), key=lambda item: item[1], reverse=True))
        return list(sorted_dict.keys())
        
        
def init_dbstock():
    params = {
        'db_name': 'stock',
        'db_user': 'user',
        'db_pwd': 'password',
        'db_host': 'ip',
        'db_port': 0
    }
    DBStock.init_db_pool(**params)
    
init_dbstock()
