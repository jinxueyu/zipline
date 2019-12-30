import tushare as ts
from trading_calendars.exchange_calendar_xshg import zh_holidays_path


def update(start_date, end_date):
    # 更新交易日历
    cal_df = ts.trade_cal()
    cal_df = cal_df[cal_df.isOpen == 1]
    cal_df = cal_df[cal_df.calendarDate >= start_date]
    cal_df = cal_df[cal_df.calendarDate <= end_date]

    # TODO 定时更新holidays写入该文件
    zh_holidays_path


if __name__ == '__main__':
    update()
