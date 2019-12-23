print("load user extension")
import sys
import os

# 得到当前根目录
o_path = os.getcwd()  # 返回当前工作目录
sys.path.append(o_path+'/.zipline/user_extensions')  # 添加自己指定的搜索路径

import pandas as pd
from zipline.data.bundles import register
from user_bundle.csv_bundle import csvdir_equities

start_session = pd.Timestamp('2012-1-3', tz='utc')
end_session = pd.Timestamp('2014-12-31', tz='utc')

register(
    'custom-csvdir-bundle',
    csvdir_equities(
        ['daily'],
        o_path+'/.zipline/user_extensions/data',
    ),
    calendar_name='NYSE',  # US equities
    start_session=start_session,
    end_session=end_session
)

from user_calendar.ex_724_calendar import EX724ExchangeCalendar
print(str(EX724ExchangeCalendar.open_time))

print("end load user extension")