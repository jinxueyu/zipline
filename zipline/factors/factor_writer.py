from datetime import date
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
import sqlite3
from factors.factor_db_schema import StockValuation, FinancialIndicator

import pandas as pd


def get_session():
    engine = create_engine('sqlite:////tmp/sqlitedb/data.db', echo=True)
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


def update_indicator_sql():
    session = get_session()
    df = pd.read_csv('~/Downloads/test_data/financial_indicator/financial_indicator.csv',  na_values=['\\N'], parse_dates=['pubDate', 'statDate', 'periodStart', 'periodEnd'], dtype={'id': int, 'pubDate': date, 'statDate':date, 'periodStart': date, 'periodEnd': date, 'reportId': int, 'eps':float,'adjusted_profit':float,'operating_profit':float,
    'value_change_profit':float,
    'roe':float,
    'inc_return':float,
    'roa':float,
    'net_profit_margin':float,
    'gross_profit_margin':float,
    'expense_to_total_revenue':float,
    'operation_profit_to_total_revenue':float,
    'net_profit_to_total_revenue':float,
    'operating_expense_to_total_revenue':float,
    'ga_expense_to_total_revenue':float,
    'financing_expense_to_total_revenue':float,
    'operating_profit_to_profit':float,
    'invesment_profit_to_profit':float,
    'adjusted_profit_to_profit':float,
    'goods_sale_and_service_to_revenue':float,
    'ocf_to_revenue':float,
    'ocf_to_operating_profit':float,
    'inc_total_revenue_year_on_year':float,
    'inc_total_revenue_annual':float,
    'inc_revenue_year_on_year':float,
    'inc_revenue_annual':float,
    'inc_operation_profit_year_on_year':float,
    'inc_operation_profit_annual':float,
    'inc_net_profit_year_on_year':float,
    'inc_net_profit_annual':float,
    'inc_net_profit_to_shareholders_year_on_year':float,
    'inc_net_profit_to_shareholders_annual':float})

    print(df.dtypes)
    for idx, row in df.iterrows():
        indicator = FinancialIndicator()
        for col in df.columns:
            val = getattr(row, col)
            if hasattr(indicator, col):
                setattr(indicator, col, val)
                # print('----------------------------')
                # print(col)
                # print(val)
                # print(type(val))

            session.add(indicator)

        print(idx)

    session.commit()
    session.close()


def update_indicator():
    conn = sqlite3.connect("/tmp/sqlitedb/data.db")
    df = pd.read_csv('~/Downloads/test_data/financial_indicator/financial_indicator.csv')
    df = df.drop(['sourceFlag'], axis=1)
    df.to_sql('financial_indicator', conn, if_exists='append', index=False)
    print('ok')


def update_stock_valuation():
    conn = sqlite3.connect("/tmp/sqlitedb/data.db")
    df = pd.read_csv('~/Downloads/test_data/stock_valuation/stock_valuation.csv')
    df = df.drop(['status', 'addTime', 'modTime'], axis=1)
    df.to_sql('stock_valuation', conn, if_exists='append', index=False)
    print('ok')

if __name__ == '__main__':
    # update_indicator()
    update_stock_valuation()
