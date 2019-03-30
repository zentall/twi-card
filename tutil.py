import os
from datetime import timedelta, timezone, datetime

JST = timezone(timedelta(hours=+9), 'JST')

def get_last_modified(file_path):
    st = os.stat(file_path).st_mtime
    dt = datetime.fromtimestamp(st, JST)
    return dt.strftime('%Y/%m/%d  %H:%M:%S')
