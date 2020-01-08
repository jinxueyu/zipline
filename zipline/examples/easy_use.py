#!/usr/bin/env python

class G:
    pass

g=G()

import logging
logging.basicConfig(level = logging.INFO, format = '%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

from zipline.api import record, symbol, set_long_only, set_max_leverage, set_benchmark
from zipline.api import order,order_target,order_value,order_percent,order_target_value,order_target_percent
from zipline.api import schedule_function,date_rules,time_rules
from zipline.finance import commission, slippage

import datetime
import pandas as pd
import numpy as np


def initialize(context):
    set_long_only()
    set_max_leverage(1)

    g.benchmark = symbol("000300.XSHG")
    set_benchmark(g.benchmark)

    context.set_commission(commission.PerShare(cost=.0007, min_trade_cost=5))
    context.set_slippage(slippage.VolumeShareSlippage())

    # schedule_function(before_trading_start,date_rules.every_day(),time_rules.market_open())

    # 用户自定义全局变量
    g.i = 0
    g.security=symbol("601901.XSHG")


def handle_data(context, data):
    log.info("handle_data speak")
    print(g.security.symbol)
    g.i+=1
    log.info("running %d days" % g.i)
    # 获取账户信息
    log.info("portfolio:")
    log.info("hold stks:%s" % context.portfolio.positions.keys())
    for s in context.portfolio.positions.keys():
        log.info("hold stk info:%s" % context.portfolio.positions[s])
    log.info("cash:%f" % context.portfolio.cash)



    ds=data.current(g.security,["price","last_traded","open","high","low","close","volume"])
    # 据我了解，zipline 拿到的最新bar是T-1日的，last_traded是T-1日的日期，如果下单会以T日的bar来撮合。这就很像是每天都在盘前交易
    # 他不显示当前日期，BarData中是有一个私有的_get_current_minute()，不能调用
    log.info("code:%s,last_traded:%s,price:%f,open:%f,high:%f,low:%f,close:%f,volume:%d" %(g.security,ds[1],ds[0],ds[2],ds[3],ds[4],ds[5],ds[6]))
    his=data.history(g.security,["price","open","high","low","close","volume"],3,"1d")
    # 数据是包含T-1日bar的
    log.info("len:%d,max_index:%s,min_index:%s" % (len(his),his.index[2],his.index[0]))
    # 多标的，多字段，取出的数据是panel field-stk-time
    pnl = data.history([symbol('601901.XSHG'), symbol('000001.XSHE')], ["close","open"], 3, "1d")
    for e in pnl:
        print("字段%s 的数据是:" % e)
        print(pnl[e])
    if g.i < 5:
        order(g.security, g.i * 1000)
    if g.i == 5:
        order_target(g.security, 0)
    record(PRICE=data.current(g.security, 'price'))


# Note: this function can be removed if running
# this algorithm on quantopian.com
def analyze(context=None, results=None):
    import matplotlib.pyplot as plt
    # Plot the portfolio and asset data.
    ax1 = plt.subplot(211)
    results.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('Portfolio value')
    ax2 = plt.subplot(212, sharex=ax1)
    results.PRICE.plot(ax=ax2)
    ax2.set_ylabel('stk price')

    # Show the plot.
    plt.gcf().set_size_inches(18, 8)
    plt.show()


# 执行命令：
# zipline run -f /Users/jiangtianyu/myCode/Foundersc/quantopian/zipline/zipline/examples/easy_use.py -b csvdir --start 2019-12-01 --end 2019-12-15 -o bqsj.pickle  --capital-base 100000