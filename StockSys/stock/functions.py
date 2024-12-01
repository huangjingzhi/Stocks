from datetime import datetime

def get_cur_day():
    now = datetime.now() # 获取当前时间
    year = now.year # 获取当前年份
    month = now.month # 获取当前月份
    day = now.day # 获取当前日期
    # 将年、月、日转换为8位数字格式
    eight_digit_time = "{:04d}{:02d}{:02d}".format(year, month, day)
    return eight_digit_time

def time_translate(t):
    date = datetime.strptime(str(t), "%Y%m%d")
    # 计算datetime类型的时间与1970年1月1日之间的时间差（以秒为单位）
    timestamp = ((date - datetime(1970, 1, 1)).total_seconds()) * 1000

    return int(timestamp)

from datetime import datetime, time

def is_work_time():
    now = datetime.now()
    weekday = now.weekday()
    start_time = time(9, 30)
    end_time = time(15, 0)

    if weekday < 5 and start_time <= now.time() <= end_time:
        return True
    else:
        return False

def is_work_night_time():
    """
    工作日的晚上
    """
    now = datetime.now()
    weekday = now.weekday()
    start_time = time(20, 30)
    end_time = time(20, 32)
    if weekday < 5 and start_time <= now.time() <= end_time:
        return True
    else:
        return False