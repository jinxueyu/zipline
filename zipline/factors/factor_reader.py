#!/usr/bin/env python
# -*- coding: utf-8 -*-
import six
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import text

import pandas as pd

from sqlalchemy.orm.query import Query

from factors.factor_db_schema import Fundamentals as indicator
from factors.factor_db_schema import Fundamentals as valuation


def get_engine():
    return create_engine('sqlite:////tmp/sqlitedb/data.db', echo=True)


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
def get_fundamentals(query, date, statDate):
    statement = query.statement
    q = statement.compile(get_engine())
    return pd.read_sql(q, con=get_engine())


if __name__ == '__main__':
    stock_pool = []
    q = query(valuation.code, valuation.market_cap, valuation.pb_ratio, valuation.ps_ratio, valuation.pe_ratio,
              indicator.roe, indicator.inc_net_profit_year_on_year, indicator.inc_total_revenue_year_on_year).outerjoin(
              indicator,
              valuation.code == indicator.code).filter(valuation.pe_ratio > 0, valuation.pb_ratio > 0, valuation.id < 100)
    # q = q.filter(valuation.pb_ratio > 0, valuation.pe_ratio > 0, indicator.roe > 0,
    #              indicator.inc_total_revenue_year_on_year > 0, valuation.code.in_(stock_pool))
    print('---------------')

    date = None

    df = get_fundamentals(q, date)
    print(df)
    # q = q.filter(valuation.pb_ratio>0,valuation.pe_ratio>0,indicator.roe>0,indicator.inc_total_revenue_year_on_year>0,valuation.code.in_(stock_pool))

    # sql_execute_result = self._engine.execute(text(sql))
    # io = six.StringIO()
    # outcsv = csv.writer(io)
    # outcsv.writerow(sql_execute_result.keys())
    # outcsv.writerows(sql_execute_result)
    # return io.getvalue()

    # print(type(q.all()))
    #
    # for i in q:
    #     print(i)
    #     break