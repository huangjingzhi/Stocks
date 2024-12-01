def stname_to_dbstandard(st_name):
    """
    ST转为指定格式: 000001.SZ -> st_000001_SZ
    """
    return "st_{}".format(st_name.replace('.', '_')).lower()

def st_dbname_to_stname(st_dbname):
    """
    ST数据库中的表格名称转文正常使用的: st_000001_SZ -> 000001.SZ
    """
    return st_dbname[3:].replace('_', '.').upper()