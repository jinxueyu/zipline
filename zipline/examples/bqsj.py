#!/usr/bin/env python

class G:
    pass


g = G()

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

from zipline.api import record, symbol, set_long_only, set_max_leverage, set_benchmark
from zipline.api import order, order_target, order_value, order_percent, order_target_value, order_target_percent
from zipline.api import schedule_function, date_rules, time_rules
from zipline.finance import commission, slippage

from zipline.factors.factor_reader import get_fundamentals, query
from zipline.factors.factor_db_schema import Fundamentals

indicator = Fundamentals
valuation = Fundamentals
balance = Fundamentals
cash_flow = Fundamentals
income = Fundamentals

import pandas as pd
import numpy as np
import datetime as dt
import statsmodels.api as sm
import copy


def initialize(context):
    # set_long_only()
    # set_max_leverage(1)

    g.benchmark = symbol("000300.XSHG")
    set_benchmark(g.benchmark)

    context.set_commission(commission.PerShare(cost=.0007, min_trade_cost=5))
    context.set_slippage(slippage.VolumeShareSlippage())
    context.universe = []

    g.i = 0
    g.count = 10
    g.tot_periods = 12
    g.days = 0
    g.periods = 0
    g.neu = False

    g.black_list = {}
    g.black_days = 40

    timing_params(context)
    # schedule_function(before_trading_start,date_rules.every_day(),time_rules.market_open())


## 择时函数参数
def timing_params(context):
    g.n = 18
    g.m = 600
    g.s = 0.5
    g.t = -0.5
    g.init = True
    g.ema_state = True
    g.rsrs_state = True
    g.LLT_state = True
    '''
    g.d1 = 8
    g.d2 = 13
    g.d3 = 21
    '''
    g.d0 = 5
    g.d1 = 8
    g.d2 = 13
    g.d3 = 21

    g.asset = symbol('000001.XSHG')
    g.position = 1.0

    g.timing = 0
    g.prev_timing = 0


def timing(context, data):
    def get_ema(context, data):
        prices = data.history(symbol('000001.XSHG'), ['close'], 500, '1d')['close']
        ema1 = pd.ewma(prices, span=g.d1).iloc[-1]
        ema2 = pd.ewma(prices, span=g.d2).iloc[-1]
        ema3 = pd.ewma(prices, span=g.d3).iloc[-1]
        # if ema0 > ema1 > ema2 > ema3:
        if ema1 > ema2 > ema3:
            g.ema_state = True
        else:
            g.ema_state = False
        log.info('g.ema_state : %s' % g.ema_state)
        return g.ema_state

    def rsrs(context, data):
        log.info('g.days,rsrs : %d' % g.days)
        if g.days == 1:
            prices = data.history(symbol('000001.XSHG'), ['high', 'low'], 500, '1d')
            highs = prices.high
            lows = prices.low
            g.ans = []
            for i in range(len(highs))[g.n:]:
                data_high = highs.iloc[i - g.n + 1:i + 1]
                data_low = lows.iloc[i - g.n + 1:i + 1]
                X = sm.add_constant(data_low)
                model = sm.OLS(data_high, X)
                results = model.fit()
                g.ans.append(results.params[1])
                section = g.ans[-g.m:]
                mu = np.mean(section)
                sigma = np.std(section)
                zscore = (section[-1] - mu) / sigma
                log.info('zscore : %f' % zscore)
                if zscore > g.s:
                    g.rsrs_state = True
                if zscore < g.t:
                    g.rsrs_state = False
                log.info('g.rsrs_state : %s' % g.rsrs_state)
        else:
            prices = data.history(symbol('000001.XSHG'), ['high', 'low'], g.n, '1d')
            highs = prices.high
            lows = prices.low
            X = sm.add_constant(lows)
            model = sm.OLS(highs, X)
            beta = model.fit().params[1]
            g.ans.append(beta)

        section = g.ans[-g.m:]
        mu = np.mean(section)
        sigma = np.std(section)
        zscore = (section[-1] - mu) / sigma
        log.info('zscore : %f' % zscore)
        if zscore > g.s:
            g.rsrs_state = True
        if zscore < g.t:
            g.rsrs_state = False
        log.info('g.rsrs_state : %s' % g.rsrs_state)
        return g.rsrs_state

    g.prev_timing = g.timing
    g.ema_state = get_ema(context, data)
    g.rsrs_state = rsrs(context, data)

    g.low_gap_state = 0  # check_gap(context,'000001.XSHG')

    g.pre_position = g.position

    if g.ema_state + g.rsrs_state == 2:
        g.position = 1.
    elif g.ema_state + g.rsrs_state == 1:
        g.position = 0.5
    else:
        g.position = 0.

    g.position = g.position * (1 - g.low_gap_state * 1)
    log.info('仓位:%s' % g.position)


def timing_manual(context):
    year = context.current_dt.year
    month = context.current_dt.month
    day = context.current_dt.day
    if (dt.date(2017, 2, 2) <= dt.date(year, month, day) <= dt.date(2017, 2, 28)) or \
        (dt.date(2017, 4, 18) <= dt.date(year, month, day) <= dt.date(2017, 5, 7)) or \
        (dt.date(2017, 11, 24) <= dt.date(year, month, day) <= dt.date(2017, 12, 19)):
        g.position = 0
    else:
        g.position = 1
    log.info('timing_manual: %d' % g.position)


def no_paused_or_st(data, stocklist):
    # zipline 没有涨跌停限制, 没有退和st
    stocks = [s for s in stocklist if data.can_trade(s)]
    return stocks


def trade(context, data, stock_list):
    security_stoploss(context)
    timing(context, data)
    for s in list(set(context.portfolio.positions.keys()) - set([symbol('511880.XSHG')])):
        if s not in stock_list:
            order_target_value(s, 0)
    val = 0
    if len(stock_list) > 0:
        val = context.portfolio.portfolio_value / len(stock_list) * g.position
    cash_val = context.portfolio.portfolio_value * (1 - g.position)
    log.info("every stk val : %f" % val)
    log.info("cash_val : %f" % cash_val)
    ups = []
    downs = []

    for s in stock_list:
        d = context.portfolio.positions.get(s, 0)
        log.info('d %s' % d)

        if d == 0 or d.amount * d.last_sale_price < val:
            ups.append(s)
        else:
            downs.append(s)

    for s in downs:
        d = context.portfolio.positions.get(s, 0)
        if d.amount * d.last_sale_price > 1.1 * val:
            log.info("sell : %s, target_value : %f" % (s, val))
            order_target_value(s, val)
    log.info('股票卖出处理完毕')
    try:
        order_target_value(symbol('511880.XSHG'), cash_val)
        log.info('try in buy money_fund,cash_val:%f' % cash_val)
    except:
        log.info('except in buy money_fund')

    for s in ups:
        d = context.portfolio.positions.get(s, 0)
        if d==0:
            log.info("buy : %s, target_value : %f" % (s,val))
            order_target_value(s, val)
        else:
            if d.amount * d.last_sale_price < 1.0 / 1.1 * val:
                log.info("buy : %s, target_value : %f" % (s, val))
                order_target_value(s, val)
    log.info('股票买入处理完毕')


def handle_data(context, data):
    meta_data = data.current(g.benchmark, ['last_traded', 'price'])
    context.current_dt = meta_data[0]
    context.previous_date = meta_data[0]
    record(benchmark=meta_data[1])

    log.info('===============================今天是策略运行第%s天' % g.days)
    log.info('当前时刻持仓股票:%s' % context.portfolio.positions.keys())
    if (g.count - g.days % g.count) != 0:
        log.info('距下次股票筛选还有%s天' % (g.count - g.days % g.count))
    else:
        log.info('今天将重新筛选股票')
    if g.days % g.count == 0:
        stocks = get_index_stocks()
        stocks = get_good(context, data, stocks, 100)
        stocks = bjsky(context, stocks)
        log.info('len(stocks):%d' % len(stocks))
        if context.universe is None or len(context.universe) == 0:
            stocks = stocks
        else:
            stocks = list(set(stocks) & set(context.universe))
        x = no_paused_or_st(data, stocks)
        log.info('输入股票池:%s' % x)
        g.stock_tobuy = x
        log.info('g.stock_tobuy = %s' % g.stock_tobuy)
        g.periods += 1
        g.days += 1
    else:
        g.days += 1
    if context.universe is None or len(context.universe) == 0:
        set_universe(context, g.stock_tobuy + [symbol('511880.XSHG')])
        log.info('context.universe : %s' % context.universe)
    trade(context, data, g.stock_tobuy)


def get_good(context, data, stock_pool, n):
    stock_pool = [s for s in stock_pool if s not in g.black_list]
    # 这里有问题的，作者想用日数据和年数据merge 在一起，可惜他们不在同一行

    stk_str_name = [s.symbol for s in stock_pool]
    q = query(valuation.code, valuation.market_cap, valuation.pb_ratio, valuation.ps_ratio, valuation.pe_ratio,
              indicator.roe, indicator.inc_net_profit_year_on_year, indicator.inc_total_revenue_year_on_year).filter(
        valuation.pe_ratio > 0, valuation.pb_ratio > 0)
    q = q.filter(valuation.pb_ratio > 0, valuation.pe_ratio > 0, indicator.roe > 0,
                 indicator.inc_total_revenue_year_on_year > 0, valuation.code.in_(stk_str_name))
    the_year = 0
    if context.current_dt.month > 5:
        the_year = context.current_dt.year - 1
    else:
        the_year = context.current_dt.year - 2
    q = q.filter(valuation.statDate == str(the_year) + "-12-31")
    df = get_fundamentals(q)
    log.info("get_good return %d lines" % len(df))
    df['code'] = df['code'].apply(lambda x: symbol(x))
    df.index = df.code.values
    df['roepb'] = df.roe / df.pb_ratio
    df['inppb'] = df.inc_net_profit_year_on_year / df.pb_ratio
    df['inrpb'] = df.inc_total_revenue_year_on_year / df.pb_ratio

    df['mmt1'] = pctchange(data, list(df.code), count=20)
    df['mmt2'] = pctchange(data, list(df.code), count=60)

    df = df.sort('pb_ratio', ascending=True)
    df['s1'] = range(len(df))
    df = df.sort('pe_ratio', ascending=True)
    df['s2'] = range(len(df))
    df = df.sort('ps_ratio', ascending=True)
    df['s3'] = range(len(df))
    df = df.sort('market_cap', ascending=True)
    df['s4'] = range(len(df))

    df = df.sort('roepb', ascending=False)
    df['s5'] = range(len(df))
    df = df.sort('inppb', ascending=False)
    df['s6'] = range(len(df))
    df = df.sort('inrpb', ascending=False)
    df['s7'] = range(len(df))
    df = df.sort('mmt1', ascending=0)
    df['s8'] = range(len(df))
    df = df.sort('mmt2', ascending=0)
    df['s9'] = range(len(df))

    df[
        'tot'] = 0.2 * df.s1 + 0.2 * df.s2 + 0.2 * df.s3 - 0.1 * df.s4 + 0.2 * df.s5 + 0.2 * df.s6 + 0.0 * df.s7 - 0.1 * df.s7 - 0.1 * df.s8
    df = df.sort('tot', ascending=True)
    return list(df.index[:n])


def bjsky(context, stock_pool):
    stk_str_name = [s.symbol for s in stock_pool]
    if context.current_dt.month > 5:
        statDate = context.current_dt.year - 1
    else:
        statDate = context.current_dt.year - 2
    q1 = query(indicator.code, valuation.pb_ratio, indicator.roe, indicator.roa, balance.total_current_liability, \
               balance.total_current_assets, balance.inventories, cash_flow.net_operate_cash_flow, income.net_profit)
    q1 = q1.filter(indicator.code.in_(stk_str_name), indicator.statDate == str(statDate) + "-12-31")
    df1 = get_fundamentals(q1)

    df1['code'] = df1['code'].apply(lambda x: symbol(x))

    df1 = df1.sort(['pb_ratio'])
    df1['current_ratio'] = df1.total_current_assets / df1.total_current_liability
    df1['quick_ratio'] = (df1.total_current_assets - df1.inventories) / df1.total_current_liability
    df1['gap'] = df1.net_operate_cash_flow - df1.net_profit
    df1.index = df1.code
    log.info('df1:')
    log.info(df1.head())

    q2 = query(indicator.code, indicator.roe, indicator.roa)
    q2 = q2.filter(indicator.code.in_(stk_str_name), indicator.statDate == str(statDate) + "-12-31")
    df = get_fundamentals(q2)

    df['code'] = df['code'].apply(lambda x: symbol(x))

    df.index = df.code
    del df['code']

    log.info('df:')
    log.info(df.head())

    df.columns = ['proe', 'proa']
    dff = pd.concat([df1, df], axis=1)
    dff['groe'] = dff.roe - dff.proe
    dff['groa'] = dff.roa - dff.proa
    dff = dff.dropna(axis=0, how='any')

    dff = dff[(dff.pb_ratio > 0) & (dff.roe > 0) & (dff.roa > 0) & (dff.gap > 0) & (dff.proe > 0) & (dff.proa > 0)]
    dff['roe_rank'] = dff['roe'].rank() + 1 * dff['groe'].rank()
    dff = dff.sort('roe_rank', ascending=0)
    log.info('dff:')
    log.info(dff.head())

    log.info('len(dff)22222 : %d ' % len(dff))
    stock_list = list(dff.index)[:5]
    return stock_list


def pctchange(data, stock, count):
    pnl = data.history(stock, ["close"], count, "1d")
    price_start = pnl['close'].fillna(method='bfill').ix[0]
    price_end = pnl['close'].fillna(method='bfill').ix[-1]
    pct = price_end / price_start - 1
    pct = pct.fillna(0)
    return pct


def security_stoploss(context):
    def black_list_update():
        if len(g.black_list) > 0:
            will_del_list = []
            for s in g.black_list.keys():
                g.black_list[s] -= 1
                if g.black_list[s] <= 0:
                    will_del_list.append(s)
            for s in will_del_list:
                del g.black_list[s]

    black_list_update()
    a = 0.15
    for s in context.portfolio.positions.keys():
        d = context.portfolio.positions.get(s, 0)
        if d.last_sale_price < (1 - a) * d.cost_basis:
            g.black_list[s] = g.black_days

    for s in g.black_list.keys():
        order_target_value(s, 0)
    log.info('g.black_list: %s ' % g.black_list)


# Note: this function can be removed if running
# this algorithm on quantopian.com
def analyze(context=None, results=None):
    import matplotlib.pyplot as plt
    # Plot the portfolio and asset data.
    ax1 = plt.subplot(211)
    results.portfolio_value.plot(ax=ax1)
    ax1.set_ylabel('Portfolio value')
    ax2 = plt.subplot(212, sharex=ax1)
    results.benchmark.plot(ax=ax2)
    ax2.set_ylabel('benchmark price')

    # Show the plot.
    plt.gcf().set_size_inches(18, 8)
    plt.show()


#### 虚拟API 这些API的实现将在未来进行
def get_index_stocks(index=None):
    stock_codes = ['000001.XSHE', '000002.XSHE', '000063.XSHE', '000069.XSHE', '000100.XSHE', '000157.XSHE',
                   '000166.XSHE', '000333.XSHE', '000338.XSHE', '000413.XSHE', '000415.XSHE', '000423.XSHE',
                   '000425.XSHE', '000538.XSHE', '000568.XSHE', '000596.XSHE', '000625.XSHE', '000627.XSHE',
                   '000629.XSHE', '000630.XSHE', '000651.XSHE', '000656.XSHE', '000661.XSHE', '000671.XSHE',
                   '000703.XSHE', '000709.XSHE', '000723.XSHE', '000725.XSHE', '000728.XSHE', '000768.XSHE',
                   '000776.XSHE', '000783.XSHE', '000786.XSHE', '000858.XSHE', '000876.XSHE', '000895.XSHE',
                   '000898.XSHE', '000938.XSHE', '000961.XSHE', '000963.XSHE', '001979.XSHE', '002001.XSHE',
                   '002007.XSHE', '002008.XSHE', '002010.XSHE', '002024.XSHE', '002027.XSHE', '002032.XSHE',
                   '002044.XSHE', '002050.XSHE', '002081.XSHE', '002120.XSHE', '002142.XSHE', '002146.XSHE',
                   '002153.XSHE', '002179.XSHE', '002202.XSHE', '002230.XSHE', '002236.XSHE', '002241.XSHE',
                   '002252.XSHE', '002271.XSHE', '002294.XSHE', '002304.XSHE', '002311.XSHE', '002352.XSHE',
                   '002410.XSHE', '002411.XSHE', '002415.XSHE', '002422.XSHE', '002456.XSHE', '002460.XSHE',
                   '002466.XSHE', '002468.XSHE', '002475.XSHE', '002493.XSHE', '002508.XSHE', '002555.XSHE',
                   '002558.XSHE', '002594.XSHE', '002601.XSHE', '002602.XSHE', '002607.XSHE', '002624.XSHE',
                   '002673.XSHE', '002714.XSHE', '002736.XSHE', '002739.XSHE', '002773.XSHE', '002841.XSHE',
                   '002916.XSHE', '002938.XSHE', '002939.XSHE', '002945.XSHE', '002958.XSHE', '300003.XSHE',
                   '300015.XSHE', '300017.XSHE', '300024.XSHE', '300033.XSHE', '300059.XSHE', '300070.XSHE',
                   '300122.XSHE', '300124.XSHE', '300136.XSHE', '300142.XSHE', '300144.XSHE', '300347.XSHE',
                   '300408.XSHE', '300413.XSHE', '300433.XSHE', '300498.XSHE', '600000.XSHG', '600004.XSHG',
                   '600009.XSHG', '600010.XSHG', '600011.XSHG', '600015.XSHG', '600016.XSHG', '600018.XSHG',
                   '600019.XSHG', '600023.XSHG', '600025.XSHG', '600027.XSHG', '600028.XSHG', '600029.XSHG',
                   '600030.XSHG', '600031.XSHG', '600036.XSHG', '600038.XSHG', '600048.XSHG', '600050.XSHG',
                   '600061.XSHG', '600066.XSHG', '600068.XSHG', '600085.XSHG', '600089.XSHG', '600100.XSHG',
                   '600104.XSHG', '600109.XSHG', '600111.XSHG', '600115.XSHG', '600118.XSHG', '600153.XSHG',
                   '600170.XSHG', '600176.XSHG', '600177.XSHG', '600183.XSHG', '600188.XSHG', '600196.XSHG',
                   '600208.XSHG', '600219.XSHG', '600221.XSHG', '600233.XSHG', '600271.XSHG', '600276.XSHG',
                   '600297.XSHG', '600299.XSHG', '600309.XSHG', '600332.XSHG', '600340.XSHG', '600346.XSHG',
                   '600352.XSHG', '600362.XSHG', '600369.XSHG', '600372.XSHG', '600383.XSHG', '600390.XSHG',
                   '600398.XSHG', '600406.XSHG', '600436.XSHG', '600438.XSHG', '600482.XSHG', '600487.XSHG',
                   '600489.XSHG', '600498.XSHG', '600516.XSHG', '600519.XSHG', '600522.XSHG', '600535.XSHG',
                   '600547.XSHG', '600566.XSHG', '600570.XSHG', '600583.XSHG', '600585.XSHG', '600588.XSHG',
                   '600606.XSHG', '600637.XSHG', '600655.XSHG', '600660.XSHG', '600663.XSHG', '600674.XSHG',
                   '600690.XSHG', '600703.XSHG', '600705.XSHG', '600733.XSHG', '600741.XSHG', '600760.XSHG',
                   '600795.XSHG', '600809.XSHG', '600816.XSHG', '600837.XSHG', '600848.XSHG', '600867.XSHG',
                   '600886.XSHG', '600887.XSHG', '600893.XSHG', '600900.XSHG', '600919.XSHG', '600926.XSHG',
                   '600928.XSHG', '600958.XSHG', '600968.XSHG', '600977.XSHG', '600989.XSHG', '600998.XSHG',
                   '600999.XSHG', '601006.XSHG', '601009.XSHG', '601012.XSHG', '601018.XSHG', '601021.XSHG',
                   '601066.XSHG', '601088.XSHG', '601108.XSHG', '601111.XSHG', '601117.XSHG', '601138.XSHG',
                   '601155.XSHG', '601162.XSHG', '601166.XSHG', '601169.XSHG', '601186.XSHG', '601198.XSHG',
                   '601211.XSHG', '601212.XSHG', '601216.XSHG', '601225.XSHG', '601229.XSHG', '601236.XSHG',
                   '601238.XSHG', '601288.XSHG', '601298.XSHG', '601318.XSHG', '601319.XSHG', '601328.XSHG',
                   '601336.XSHG', '601360.XSHG', '601377.XSHG', '601390.XSHG', '601398.XSHG', '601555.XSHG',
                   '601577.XSHG', '601600.XSHG', '601601.XSHG', '601607.XSHG', '601618.XSHG', '601628.XSHG',
                   '601633.XSHG', '601668.XSHG', '601669.XSHG', '601688.XSHG', '601698.XSHG', '601727.XSHG',
                   '601766.XSHG', '601788.XSHG', '601800.XSHG', '601808.XSHG', '601818.XSHG', '601828.XSHG',
                   '601838.XSHG', '601857.XSHG', '601877.XSHG', '601878.XSHG', '601881.XSHG', '601888.XSHG',
                   '601898.XSHG', '601899.XSHG', '601901.XSHG', '601919.XSHG', '601933.XSHG', '601939.XSHG',
                   '601985.XSHG', '601988.XSHG', '601989.XSHG', '601992.XSHG', '601997.XSHG', '601998.XSHG',
                   '603019.XSHG', '603156.XSHG', '603160.XSHG', '603259.XSHG', '603260.XSHG', '603288.XSHG',
                   '603501.XSHG', '603799.XSHG', '603833.XSHG', '603899.XSHG', '603986.XSHG', '603993.XSHG']
    # stock_codes = ['000001.XSHE', '000002.XSHE']
    stock_pool = [symbol(c) for c in stock_codes]
    return stock_pool


def set_universe(context, stk_list):
    context.universe = stk_list
