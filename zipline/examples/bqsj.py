#!/usr/bin/env python


import pandas as pd
import numpy as np
import datetime as dt
import statsmodels.api as sm
import copy

from zipline.api import order_target, record, symbol
from zipline.api import schedule_function, date_rules,time_rules
from zipline.protocol import BarData
from zipline.finance import commission, slippage



def initialize(context):
    context.i = 0
    context.set_commission(commission.PerShare(cost=.0075, min_trade_cost=1.0))
    context.set_slippage(slippage.VolumeShareSlippage())

    context.count = 10
    context.tot_periods = 12
    context.days = 0
    context.periods = 0
    context.neu = False

    context.black_list = {}
    context.black_days = 40

    timing_params(context)
    schedule_function(handle_data,date_rules.every_day(),time_rules.market_open(hours=1,minutes=30))


## 择时函数参数
def timing_params(context):
    context.n = 18
    context.m = 600
    context.s = 0.5
    context.t = -0.5
    context.init = True
    context.ema_state = True
    context.rsrs_state = True
    context.LLT_state = True
    '''
    context.d1 = 8
    context.d2 = 13
    context.d3 = 21
    '''
    context.d0 = 5
    context.d1 = 8
    context.d2 = 13
    context.d3 = 21

    context.asset = '000001.XSHG'
    context.position = 1.0

    context.timing = 0
    context.prev_timing = 0

def handle_data(context, data):
    print(data.current(symbol("000001.XSHE"),["price","last_traded","open","high","low","close","volume"]))
    # Skip first 300 days to get full windows
    context.i += 1
    if context.i < 300:
        return
    print(context.i)
























# # Note: this function can be removed if running
# # this algorithm on quantopian.com
# def analyze(context=None, results=None):
#     import matplotlib.pyplot as plt
#     import logbook
#     logbook.StderrHandler().push_application()
#     log = logbook.Logger('Algorithm')
#
#     fig = plt.figure()
#     ax1 = fig.add_subplot(211)
#     results.portfolio_value.plot(ax=ax1)
#     ax1.set_ylabel('Portfolio value (USD)')
#
#     ax2 = fig.add_subplot(212)
#     ax2.set_ylabel('Price (USD)')
#
#     # If data has been record()ed, then plot it.
#     # Otherwise, log the fact that no data has been recorded.
#     if ('AAPL' in results and 'short_mavg' in results and
#             'long_mavg' in results):
#         results['AAPL'].plot(ax=ax2)
#         results[['short_mavg', 'long_mavg']].plot(ax=ax2)
#
#         trans = results.ix[[t != [] for t in results.transactions]]
#         buys = trans.ix[[t[0]['amount'] > 0 for t in
#                          trans.transactions]]
#         sells = trans.ix[
#             [t[0]['amount'] < 0 for t in trans.transactions]]
#         ax2.plot(buys.index, results.short_mavg.ix[buys.index],
#                  '^', markersize=10, color='m')
#         ax2.plot(sells.index, results.short_mavg.ix[sells.index],
#                  'v', markersize=10, color='k')
#         plt.legend(loc=0)
#     else:
#         msg = 'AAPL, short_mavg & long_mavg data not captured using record().'
#         ax2.annotate(msg, xy=(0.1, 0.5))
#         log.info(msg)
#
#     plt.show()


