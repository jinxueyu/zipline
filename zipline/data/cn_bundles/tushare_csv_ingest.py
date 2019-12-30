import os

import click
import tushare as ts

from trading_calendars import get_calendar
from zipline.data import bundles
from zipline.data.bundles import register
from zipline.data.bundles.csvdir import csvdir_equities

start_session = None #pd.Timestamp('2016-1-1', tz='utc')
end_session = None #pd.Timestamp('2018-1-1', tz='utc')

register(
    'cn-csvdir-bundle',
    csvdir_equities(
        ['daily']
    ),
    calendar_name='XSHG',
    start_session=start_session,
    end_session=end_session
)

ts.set_token('0ff0874e8b9b05e2fd0ea35396e83a0172d1d4a89c4451fe51c8704a')


def get_trading_days(trading_calendar, start_date, end_date):
    # 交易日历
    # cal = XSHGExchangeCalendar(start=start_date, end=end_date)
    trading_days = get_calendar(trading_calendar).all_sessions
    trading_days = trading_days[trading_days.slice_indexer(start_date, end_date)]
    print(trading_days)
    return trading_days


def get_bar_data(stock_code, start_date, end_date):
    pro = ts.pro_api()

    hist_df = pro.daily(ts_code=stock_code, start_date=start_date.replace('-', ''), end_date=end_date.replace('-', ''))
    # hist_df = ts.get_hist_data(stock_code, start=start_date, end=end_date)
    hist_df = hist_df[['trade_date', 'open', 'high', 'low', 'close', 'vol']]
    hist_df.trade_date = hist_df.trade_date.map(lambda x: x[0:4]+'-'+x[4:6]+'-'+x[6:])
    hist_df.index = hist_df.trade_date
    hist_df = hist_df.drop(['trade_date'], axis=1)

    # TODO 补充拆股、分红等信息
    hist_df['dividend'] = 0.0
    hist_df['split'] = 1.0

    return hist_df


def get_stock_list():
    pro = ts.pro_api()
    data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    return data.ts_code


@click.group()
@click.option(
    '-e',
    '--extension',
    multiple=True,
    help='File or module path to a zipline extension to load.',
)
def main(extension):
    pass


@main.command()
@click.option(
    '-c',
    '--stock_code',
    default='__ALL__',
    help='The stock to ingest.',
)
@click.option(
    '--data-frequency',
    type=click.Choice({'daily', 'minute'}),
    default='daily',
    show_default=True,
    help='The data frequency of the simulation.',
)
@click.option(
    '-b',
    '--bundle',
    default='quandl',
    metavar='BUNDLE-NAME',
    show_default=True,
    help='The data bundle for ingest.',
)
@click.option(
    '-s',
    '--start',
    help='The start date of bar.',
)
@click.option(
    '-e',
    '--end',
    help='The end date of bar.',
)
@click.option(
    '--trading-calendar',
    metavar='TRADING-CALENDAR',
    default='XSHG',
    help="The calendar you want to use e.g. XLON. XSHG is the default."
)
def ingest(bundle, data_frequency, stock_code, start, end, trading_calendar):
    csv_dir = '/tmp/bundles/csv_dir/'
    os.environ.setdefault('CSVDIR', csv_dir)

    if stock_code == '__ALL__':
        stock_codes = get_stock_list()
    else:
        stock_codes = [stock_code]

    for stock_code in stock_codes:
        print('download %s ' % stock_code)
        download_bar_data(data_frequency, stock_code, start, end, trading_calendar)

    bundles.ingest(bundle, os.environ, show_progress=True)


def download_bar_data(data_frequency, stock_code, start, end, trading_calendar):

    # 取历史行情
    hist_df = get_bar_data(stock_code, start, end)

    # 交易日历
    trading_days = get_trading_days(trading_calendar, start, end)
    trading_days = trading_days.map(lambda x: x.strftime('%Y-%m-%d'))

    # 补充停牌时间段内数据
    hist_df = hist_df.reindex(trading_days, copy=False).fillna(0.0)
    hist_df.rename(columns={'vol': 'volume'}, inplace=True)

    # temp dir
    csv_dir = os.environ.get('CSVDIR')
    hist_df.to_csv(csv_dir+'/'+data_frequency+'/'+stock_code+'.csv', sep=',', header=True, index=True)


if __name__ == '__main__':
    main()
