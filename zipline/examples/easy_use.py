#!/usr/bin/env python

class G:
    pass

g=G()

from zipline.api import record, symbol
from zipline.api import order,order_target,order_value,order_percent,order_target_value,order_target_percent
from zipline.api import schedule_function,date_rules,time_rules
from zipline.finance import commission, slippage

import datetime
import pandas as pd
import numpy as np


def initialize(context):

    context.set_commission(commission.PerShare(cost=.0007, min_trade_cost=5))
    context.set_slippage(slippage.VolumeShareSlippage())
    context.set_benchmark(symbol("000300.XSHG"))

    # schedule_function(before_trading_start,date_rules.every_day(),time_rules.market_open())

    # 用户自定义全局变量
    g.i = 0
    g.security=symbol("601901.XSHG")


def handle_data(context, data):
    print("handle_data speak")
    g.i+=1
    print("running %d days" % g.i)
    ds=data.current(g.security,["price","last_traded","open","high","low","close","volume"])
    print("code:%s,last_traded:%s,price:%f,open:%f,high:%f,low:%f,close:%f,volume:%d" %(g.security,ds[1],ds[0],ds[2],ds[3],ds[4],ds[5],ds[6]))
    his=data.history(g.security,["price","open","high","low","close","volume"],3,"1d")
    print(his)
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