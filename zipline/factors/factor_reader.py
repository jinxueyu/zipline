#!/usr/bin/env python
# -*- coding: utf-8 -*-
import six
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import text
from pytz import timezone

from zipline.factors.factor_db_schema import Fundamentals
indicator=Fundamentals
valuation=Fundamentals

def get_engine():
    return create_engine('sqlite:////Users/jiangtianyu/ziplinedata/sqlitedb/data.db', echo=False)


def get_session():
    engine = get_engine()
    session = sessionmaker(bind=engine)

    return session()


def query(*args, **kwargs):
    """
    获取一个Query对象, 传给 get_fundamentals

    具体使用方法请参考http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html#querying

    示例: 查询'000001.XSHE'的所有市值数据, 时间是2015-10-15
    q = query(
        valuation
    ).filter(
        valuation.code == '000001.XSHE'
    )
    get_fundamentals(q, '2015-10-15')
    """
    return get_session().query(*args, **kwargs)


# Query_filter = Query.filter
#
# def my_filter(self, *criterions):
#     criterions = list(criterions)
#     for criterion in criterions:
#         if criterion in (True, False):
#             raise Exception(invalid_criterion_msg)
#     return Query_filter(self, *criterions)
#
# Query.filter = my_filter


def query(*args, **kwargs):
    """
    获取一个Query对象, 传给 get_fundamentals

    具体使用方法请参考http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html#querying

    示例: 查询'000001.XSHE'的所有市值数据, 时间是2015-10-15
    q = query(
        valuation
    ).filter(
        valuation.code == '000001.XSHE'
    )
    get_fundamentals(q, '2015-10-15')
    """
    return get_session().query(*args, **kwargs)

# TODO date 从外面传
def get_fundamentals(query):
    statement = query.statement
    q = statement.compile(get_engine())
    return pd.read_sql(q, con=get_engine())


if __name__ == '__main__':
    # 显示所有列
    pd.set_option('display.max_columns', None)
    # 显示所有行
    pd.set_option('display.max_rows', None)
    # 设置value的显示长度为100，默认为50
    pd.set_option('max_colwidth', 100)
    # 不要折行
    pd.set_option('expand_frame_repr', False)

    the_date="2018-12-31"
    stock_pool=['000001.XSHE','000002.XSHE','000063.XSHE','000069.XSHE','000100.XSHE','000157.XSHE','000166.XSHE','000333.XSHE','000338.XSHE','000413.XSHE','000415.XSHE','000423.XSHE','000425.XSHE','000538.XSHE','000568.XSHE','000596.XSHE','000625.XSHE','000627.XSHE','000629.XSHE','000630.XSHE','000651.XSHE','000656.XSHE','000661.XSHE','000671.XSHE','000703.XSHE','000709.XSHE','000723.XSHE','000725.XSHE','000728.XSHE','000768.XSHE','000776.XSHE','000783.XSHE','000786.XSHE','000858.XSHE','000876.XSHE','000895.XSHE','000898.XSHE','000938.XSHE','000961.XSHE','000963.XSHE','001979.XSHE','002001.XSHE','002007.XSHE','002008.XSHE','002010.XSHE','002024.XSHE','002027.XSHE','002032.XSHE','002044.XSHE','002050.XSHE','002081.XSHE','002120.XSHE','002142.XSHE','002146.XSHE','002153.XSHE','002179.XSHE','002202.XSHE','002230.XSHE','002236.XSHE','002241.XSHE','002252.XSHE','002271.XSHE','002294.XSHE','002304.XSHE','002311.XSHE','002352.XSHE','002410.XSHE','002411.XSHE','002415.XSHE','002422.XSHE','002456.XSHE','002460.XSHE','002466.XSHE','002468.XSHE','002475.XSHE','002493.XSHE','002508.XSHE','002555.XSHE','002558.XSHE','002594.XSHE','002601.XSHE','002602.XSHE','002607.XSHE','002624.XSHE','002673.XSHE','002714.XSHE','002736.XSHE','002739.XSHE','002773.XSHE','002841.XSHE','002916.XSHE','002938.XSHE','002939.XSHE','002945.XSHE','002958.XSHE','300003.XSHE','300015.XSHE','300017.XSHE','300024.XSHE','300033.XSHE','300059.XSHE','300070.XSHE','300122.XSHE','300124.XSHE','300136.XSHE','300142.XSHE','300144.XSHE','300347.XSHE','300408.XSHE','300413.XSHE','300433.XSHE','300498.XSHE','600000.XSHG','600004.XSHG','600009.XSHG','600010.XSHG','600011.XSHG','600015.XSHG','600016.XSHG','600018.XSHG','600019.XSHG','600023.XSHG','600025.XSHG','600027.XSHG','600028.XSHG','600029.XSHG','600030.XSHG','600031.XSHG','600036.XSHG','600038.XSHG','600048.XSHG','600050.XSHG','600061.XSHG','600066.XSHG','600068.XSHG','600085.XSHG','600089.XSHG','600100.XSHG','600104.XSHG','600109.XSHG','600111.XSHG','600115.XSHG','600118.XSHG','600153.XSHG','600170.XSHG','600176.XSHG','600177.XSHG','600183.XSHG','600188.XSHG','600196.XSHG','600208.XSHG','600219.XSHG','600221.XSHG','600233.XSHG','600271.XSHG','600276.XSHG','600297.XSHG','600299.XSHG','600309.XSHG','600332.XSHG','600340.XSHG','600346.XSHG','600352.XSHG','600362.XSHG','600369.XSHG','600372.XSHG','600383.XSHG','600390.XSHG','600398.XSHG','600406.XSHG','600436.XSHG','600438.XSHG','600482.XSHG','600487.XSHG','600489.XSHG','600498.XSHG','600516.XSHG','600519.XSHG','600522.XSHG','600535.XSHG','600547.XSHG','600566.XSHG','600570.XSHG','600583.XSHG','600585.XSHG','600588.XSHG','600606.XSHG','600637.XSHG','600655.XSHG','600660.XSHG','600663.XSHG','600674.XSHG','600690.XSHG','600703.XSHG','600705.XSHG','600733.XSHG','600741.XSHG','600760.XSHG','600795.XSHG','600809.XSHG','600816.XSHG','600837.XSHG','600848.XSHG','600867.XSHG','600886.XSHG','600887.XSHG','600893.XSHG','600900.XSHG','600919.XSHG','600926.XSHG','600928.XSHG','600958.XSHG','600968.XSHG','600977.XSHG','600989.XSHG','600998.XSHG','600999.XSHG','601006.XSHG','601009.XSHG','601012.XSHG','601018.XSHG','601021.XSHG','601066.XSHG','601088.XSHG','601108.XSHG','601111.XSHG','601117.XSHG','601138.XSHG','601155.XSHG','601162.XSHG','601166.XSHG','601169.XSHG','601186.XSHG','601198.XSHG','601211.XSHG','601212.XSHG','601216.XSHG','601225.XSHG','601229.XSHG','601236.XSHG','601238.XSHG','601288.XSHG','601298.XSHG','601318.XSHG','601319.XSHG','601328.XSHG','601336.XSHG','601360.XSHG','601377.XSHG','601390.XSHG','601398.XSHG','601555.XSHG','601577.XSHG','601600.XSHG','601601.XSHG','601607.XSHG','601618.XSHG','601628.XSHG','601633.XSHG','601668.XSHG','601669.XSHG','601688.XSHG','601698.XSHG','601727.XSHG','601766.XSHG','601788.XSHG','601800.XSHG','601808.XSHG','601818.XSHG','601828.XSHG','601838.XSHG','601857.XSHG','601877.XSHG','601878.XSHG','601881.XSHG','601888.XSHG','601898.XSHG','601899.XSHG','601901.XSHG','601919.XSHG','601933.XSHG','601939.XSHG','601985.XSHG','601988.XSHG','601989.XSHG','601992.XSHG','601997.XSHG','601998.XSHG','603019.XSHG','603156.XSHG','603160.XSHG','603259.XSHG','603260.XSHG','603288.XSHG','603501.XSHG','603799.XSHG','603833.XSHG','603899.XSHG','603986.XSHG','603993.XSHG']
    q = query(valuation.code,valuation.day,valuation.statDate,valuation.pubDate, valuation.market_cap, valuation.pb_ratio, valuation.ps_ratio, valuation.pe_ratio,
              indicator.roe,indicator.inc_net_profit_year_on_year, indicator.inc_total_revenue_year_on_year
              ).filter(valuation.code.in_(stock_pool), valuation.statDate == the_date)
    q = q.filter(valuation.pb_ratio > 0, valuation.pe_ratio > 0, indicator.roe > 0, indicator.inc_total_revenue_year_on_year > 0)
    df = get_fundamentals(q.order_by(valuation.day))
    print(df)