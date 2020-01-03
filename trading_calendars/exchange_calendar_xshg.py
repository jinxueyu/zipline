import sys, os

from datetime import time
import pandas as pd
from pytz import timezone
from .precomputed_trading_calendar import PrecomputedTradingCalendar

zh_holidays_path = os.path.dirname(os.path.abspath(__file__))+'/xshg_holidays.csv'

precomputed_shanghai_holidays = pd.to_datetime(pd.read_csv(zh_holidays_path, header=None).values[:, 0])


class XSHGExchangeCalendar(PrecomputedTradingCalendar):
    """
    Exchange calendar for the Shanghai Stock Exchange (XSHG, XSSC, SSE).

    Open time: 9:30 Asia/Shanghai
    Close time: 15:00 Asia/Shanghai

    NOTE: For now, we are skipping the intra-day break from 11:30 to 13:00.

    Due to the complexity around the Shanghai exchange holidays, we are
    hardcoding a list of holidays covering 1999-2025, inclusive. There are
    no known early closes or late opens.
    """

    name = "XSHG"
    tz = timezone("Asia/Shanghai")
    open_times = (
        (None, time(9, 31)),
    )
    close_times = (
        (None, time(15, 0)),
    )

    @property
    def precomputed_holidays(self):
        return precomputed_shanghai_holidays
