import sqlite3
import pandas as pd
from stock import stfuns
from stock import config as cfg
import time
import sys
class Stock:
    def __init__(self, name):
        self.name = name
        self.db = cfg.ST_DB_NAME
        self.db_name = stfuns.stname_to_dbstandard(st_name=name)
        self.conn = sqlite3.connect("{}.db".format(cfg.ST_DB_NAME))
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS {} 
                            (trade_date TEXT PRIMARY KEY, 
                                open REAL, 
                                high REAL, 
                                low REAL, 
                                close REAL, 
                                pre_close REAL, 
                                change REAL, 
                                pct_chg REAL, 
                                vol REAL, 
                                amount REAL)'''.format(self.db_name))
        self.conn.commit()

    def __del__(self):
        self.conn.close()

    def add_data(self, trade_date, open, high, low, close, pre_close, change, pct_chg, vol, amount):
        self.cursor.execute('''INSERT OR REPLACE INTO {}
                               (trade_date, open, high, low, close, pre_close, change, pct_chg, vol, amount)
                               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''.format(self.db_name),
                            (trade_date, open, high, low, close, pre_close, change, pct_chg, vol, amount))
        self.conn.commit()

    def delete_data(self, trade_date):
        self.cursor.execute("DELETE FROM {} WHERE trade_date=?".format(self.db_name), (trade_date,))
        self.conn.commit()

    def update_data(self, trade_date, open=None, high=None, low=None, close=None, pre_close=None, change=None, pct_chg=None, vol=None, amount=None):
        updates = []
        if open is not None:
            updates.append(f"open={open}")
        if high is not None:
            updates.append(f"high={high}")
        if low is not None:
            updates.append(f"low={low}")
        if close is not None:
            updates.append(f"close={close}")
        if pre_close is not None:
            updates.append(f"pre_close={pre_close}")
        if change is not None:
            updates.append(f"change={change}")
        if pct_chg is not None:
            updates.append(f"pct_chg={pct_chg}")
        if vol is not None:
            updates.append(f"vol={vol}")
        if amount is not None:
            updates.append(f"amount={amount}")
        update_str = ", ".join(updates)
        self.cursor.execute(f"UPDATE {self.db_name} SET {update_str} WHERE trade_date=?", (trade_date,))
        self.conn.commit()

    def get_dataframe(self, n_days):
        self.cursor.execute(f"SELECT * FROM {self.db_name} ORDER BY trade_date DESC LIMIT {n_days}")
        data = self.cursor.fetchall()
        df = pd.DataFrame(data, columns=['trade_date', 'open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg', 'vol', 'amount'])
        df = df.sort_values('trade_date', ascending=True).reset_index(drop=True)
        return df

    def get_dict(self, trade_date):
        self.cursor.execute("SELECT * FROM {} WHERE trade_date=?".format(self.db_name), (trade_date,))
        data = self.cursor.fetchone()
        if data is None:
            return None
        else:
            return {'trade_date': data[0], 'open': data[1], 'high': data[2], 'low': data[3], 'close': data[4],
                    'pre_close': data[5], 'change': data[6], 'pct_chg': data[7], 'vol': data[8], 'amount': data[9]}

    @staticmethod
    def get_all_stocks():
        conn = sqlite3.connect('{}.db'.format(cfg.ST_DB_NAME))
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        stocks = cursor.fetchall()
        conn.close()
        return [stfuns.st_dbname_to_stname(s[0]) for s in stocks]

    @staticmethod
    def remove_stock(name):
        """
        需要使用删除表操作
        """
        conn = sqlite3.connect('{}.db'.format(cfg.ST_DB_NAME))
        cursor = conn.cursor()
        cursor.execute(f"DROP TABLE IF EXISTS {name}")
        conn.commit()
        conn.close()

    @staticmethod
    def get_recent_data(name, days):
        # 获取所有数据
        conn = sqlite3.connect('{}.db'.format(cfg.ST_DB_NAME))
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {name}")
        rows = cur.fetchall()
        conn.close()
        # 选择最近的n天数据
        recent_rows = rows[-days:]
        # 转换为DataFrame格式
        df = pd.DataFrame(recent_rows, columns=['trade_date', 'open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg', 'vol', 'amount'])
        return df

    @staticmethod
    def get_recent_data(name, days):
        # 获取所有数据
        conn = sqlite3.connect('{}.db'.format(cfg.ST_DB_NAME))
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {name}")
        rows = cur.fetchall()
        conn.close()

        # 选择最近的n天数据
        recent_rows = rows[-days:]

        # 转换为DataFrame格式
        df = pd.DataFrame(recent_rows, columns=['trade_date', 'open', 'high', 'low', 'close', 'pre_close', 'change', 'pct_chg', 'vol', 'amount'])
        return df