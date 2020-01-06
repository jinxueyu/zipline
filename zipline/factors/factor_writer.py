from datetime import date
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
import sqlite3
# from factors.factor_db_schema import StockValuation, FinancialIndicator

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

# def update_tb_fundamentals():
#     conn = sqlite3.connect("/tmp/sqlitedb/data.db")
#     df = pd.read_csv('~/Downloads/financial_all/financial_all_2015_2020.csv')
#     df.to_sql('tb_fundamentals', conn, if_exists='append', index=False)
#     print('ok')

data_type_mapping={
'code':object,
'day':object,
'statDate':object,
'pubDate':object,
'capitalization':float,
'circulating_cap':float,
'market_cap':float,
'circulating_market_cap':float,
'turnover_ratio':float,
'pe_ratio':float,
'pe_ratio_lyr':float,
'pb_ratio':float,
'ps_ratio':float,
'pcf_ratio':float,
'total_operating_revenue':float,
'operating_revenue':float,
'interest_income':float,
'premiums_earned':float,
'commission_income':float,
'total_operating_cost':float,
'operating_cost':float,
'interest_expense':float,
'commission_expense':float,
'refunded_premiums':float,
'net_pay_insurance_claims':float,
'withdraw_insurance_contract_reserve':float,
'policy_dividend_payout':float,
'reinsurance_cost':float,
'operating_tax_surcharges':float,
'sale_expense':float,
'administration_expense':float,
'financial_expense':float,
'asset_impairment_loss':float,
'fair_value_variable_income':float,
'investment_income':float,
'invest_income_associates':float,
'exchange_income':float,
'operating_profit':float,
'non_operating_revenue':float,
'non_operating_expense':float,
'disposal_loss_non_current_liability':float,
'total_profit':float,
'income_tax_expense':float,
'net_profit':float,
'np_parent_company_owners':float,
'minority_profit':float,
'basic_eps':float,
'diluted_eps':float,
'other_composite_income':float,
'total_composite_income':float,
'ci_parent_company_owners':float,
'ci_minority_owners':float,
'cash_equivalents':float,
'settlement_provi':float,
'lend_capital':float,
'trading_assets':float,
'bill_receivable':float,
'account_receivable':float,
'advance_payment':float,
'insurance_receivables':float,
'reinsurance_receivables':float,
'reinsurance_contract_reserves_receivable':float,
'interest_receivable':float,
'dividend_receivable':float,
'other_receivable':float,
'bought_sellback_assets':float,
'inventories':float,
'non_current_asset_in_one_year':float,
'other_current_assets':float,
'total_current_assets':float,
'loan_and_advance':float,
'hold_for_sale_assets':float,
'hold_to_maturity_investments':float,
'longterm_receivable_account':float,
'longterm_equity_invest':float,
'investment_property':float,
'fixed_assets':float,
'constru_in_process':float,
'construction_materials':float,
'fixed_assets_liquidation':float,
'biological_assets':float,
'oil_gas_assets':float,
'intangible_assets':float,
'development_expenditure':float,
'good_will':float,
'long_deferred_expense':float,
'deferred_tax_assets':float,
'other_non_current_assets':float,
'total_non_current_assets':float,
'total_assets':float,
'shortterm_loan':float,
'borrowing_from_centralbank':float,
'deposit_in_interbank':float,
'borrowing_capital':float,
'trading_liability':float,
'notes_payable':float,
'accounts_payable':float,
'advance_peceipts':float,
'sold_buyback_secu_proceeds':float,
'commission_payable':float,
'salaries_payable':float,
'taxs_payable':float,
'interest_payable':float,
'dividend_payable':float,
'other_payable':float,
'reinsurance_payables':float,
'insurance_contract_reserves':float,
'proxy_secu_proceeds':float,
'receivings_from_vicariously_sold_securities':float,
'non_current_liability_in_one_year':float,
'other_current_liability':float,
'total_current_liability':float,
'longterm_loan':float,
'bonds_payable':float,
'longterm_account_payable':float,
'specific_account_payable':float,
'estimate_liability':float,
'deferred_tax_liability':float,
'other_non_current_liability':float,
'total_non_current_liability':float,
'total_liability':float,
'paidin_capital':float,
'capital_reserve_fund':float,
'treasury_stock':float,
'specific_reserves':float,
'surplus_reserve_fund':float,
'ordinary_risk_reserve_fund':float,
'retained_profit':float,
'foreign_currency_report_conv_diff':float,
'equities_parent_company_owners':float,
'minority_interests':float,
'total_owner_equities':float,
'total_sheet_owner_equities':float,
'goods_sale_and_service_render_cash':float,
'net_deposit_increase':float,
'net_borrowing_from_central_bank':float,
'net_borrowing_from_finance_co':float,
'net_original_insurance_cash':float,
'net_cash_received_from_reinsurance_business':float,
'net_insurer_deposit_investment':float,
'net_deal_trading_assets':float,
'interest_and_commission_cashin':float,
'net_increase_in_placements':float,
'net_buyback':float,
'tax_levy_refund':float,
'other_cashin_related_operate':float,
'subtotal_operate_cash_inflow':float,
'goods_and_services_cash_paid':float,
'net_loan_and_advance_increase':float,
'net_deposit_in_cb_and_ib':float,
'original_compensation_paid':float,
'handling_charges_and_commission':float,
'policy_dividend_cash_paid':float,
'staff_behalf_paid':float,
'tax_payments':float,
'other_operate_cash_paid':float,
'subtotal_operate_cash_outflow':float,
'net_operate_cash_flow':float,
'invest_withdrawal_cash':float,
'invest_proceeds':float,
'fix_intan_other_asset_dispo_cash':float,
'net_cash_deal_subcompany':float,
'other_cash_from_invest_act':float,
'subtotal_invest_cash_inflow':float,
'fix_intan_other_asset_acqui_cash':float,
'invest_cash_paid':float,
'impawned_loan_net_increase':float,
'net_cash_from_sub_company':float,
'other_cash_to_invest_act':float,
'subtotal_invest_cash_outflow':float,
'net_invest_cash_flow':float,
'cash_from_invest':float,
'cash_from_mino_s_invest_sub':float,
'cash_from_borrowing':float,
'cash_from_bonds_issue':float,
'other_finance_act_cash':float,
'subtotal_finance_cash_inflow':float,
'borrowing_repayment':float,
'dividend_interest_payment':float,
'proceeds_from_sub_to_mino_s':float,
'other_finance_act_payment':float,
'subtotal_finance_cash_outflow':float,
'net_finance_cash_flow':float,
'exchange_rate_change_effect':float,
'cash_equivalent_increase':float,
'cash_equivalents_at_beginning':float,
'cash_and_equivalents_at_end':float,
'eps':float,
'adjusted_profit':float,
'operating_earnings':float,
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
'inc_net_profit_to_shareholders_annual':float,
}

def update_tb_fundamentals():
    conn = sqlite3.connect("/tmp/sqlitedb/data.db")
    df = pd.read_csv('/Users/jiangtianyu/ziplinedata/financial/financial_all/financial_all_2015_2019.csv',na_values=['\\N'],dtype=data_type_mapping)

    df.to_sql('tb_fundamentals', conn, if_exists='append', index=False)
    print('ok')

if __name__ == '__main__':
    # update_indicator()
    # update_stock_valuation()
    update_tb_fundamentals()
