# coding: utf-8
from sqlalchemy import Column, Date, DateTime, Float, Index, Integer, String, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

__all__ = [
    'BalanceSheet',
    'CashFlowStatement',
    'IncomeStatement',
    'StockValuation',
    'FinancialIndicator',
    'BankIndicatorAcc',
    'SecurityIndicatorAcc',
    'InsuranceIndicatorAcc',
]

Base = declarative_base()
metadata = Base.metadata


class Fundamentals(Base):
    """
    负债表
    """

    __tablename__ = 'tb_fundamentals'
    # __table_args__ = (
    #     Index('idx_day_code', 'day', 'code', unique=True),
    # )

    id = Column(Integer, primary_key=True)
    code = Column(String(12), nullable=False, doc="股票代码(带后缀: .XSHE/.XSHG)")
    day = Column(Date, nullable=False, server_default=text("'0000-00-00'"), doc="日期")
    pubDate = Column(Date, nullable=False, server_default=text("'0000-00-00'"))
    statDate = Column(Date, nullable=False, server_default=text("'0000-00-00'"))
    # periodStart = Column(Date, nullable=False, server_default=text("'0000-00-00'"), doc="两次报告之间的日期范围:start date")
    # periodEnd = Column(Date, nullable=False, server_default=text("'0000-00-00'"), doc="两次报告之间的日期范围:end date")
    reportId = Column(Integer, nullable=False, server_default=text("'0'"))
    cash_equivalents = Column(Float(20), doc="货币资金(元)")
    settlement_provi = Column(Float(20), doc="结算备付金(元)")
    lend_capital = Column(Float(20), doc="拆出资金(元)")
    trading_assets = Column(Float(20), doc="交易性金融资产(元)")
    bill_receivable = Column(Float(20), doc="应收票据(元)")
    account_receivable = Column(Float(20), doc="应收账款(元)")
    advance_payment = Column(Float(20), doc="预付款项(元)")
    insurance_receivables = Column(Float(20), doc="应收保费(元)")
    reinsurance_receivables = Column(Float(20), doc="应收保费(元)")
    reinsurance_contract_reserves_receivable = Column(Float(20), doc="应收分保合同准备金(元)")
    interest_receivable = Column(Float(20), doc="应收利息(元)")
    dividend_receivable = Column(Float(20), doc="应收股利(元)")
    other_receivable = Column(Float(20), doc="其他应收款(元)")
    bought_sellback_assets = Column(Float(20), doc="买入返售金融资产(元)")
    inventories = Column(Float(20), doc="存货(元)")
    non_current_asset_in_one_year = Column(Float(20), doc="年份")
    other_current_assets = Column(Float(20), doc="其他流动资产(元)")
    total_current_assets = Column(Float(20), doc="流动资产合计(元)")
    loan_and_advance = Column(Float(20), doc="发放委托贷款及垫款(元)")
    hold_for_sale_assets = Column(Float(20), doc="可供出售金融资产(元)")
    hold_to_maturity_investments = Column(Float(20), doc="持有至到期投资(元)")
    longterm_receivable_account = Column(Float(20), doc="长期应收款(元)")
    longterm_equity_invest = Column(Float(20), doc="长期股权投资(元)")
    investment_property = Column(Float(20), doc="投资性房地产(元)")
    fixed_assets = Column(Float(20), doc="固定资产(元)")
    constru_in_process = Column(Float(20), doc="在建工程(元)")
    construction_materials = Column(Float(20), doc="工程物资(元)")
    fixed_assets_liquidation = Column(Float(20), doc="固定资产清理(元)")
    biological_assets = Column(Float(20), doc="生产性生物资产(元)")
    oil_gas_assets = Column(Float(20), doc="油气资产(元)")
    intangible_assets = Column(Float(20), doc="无形资产(元)")
    development_expenditure = Column(Float(20), doc="开发支出(元)")
    good_will = Column(Float(20), doc="商誉(元)")
    long_deferred_expense = Column(Float(20), doc="长期待摊费用(元)")
    deferred_tax_assets = Column(Float(20), doc="递延所得税资产(元)")
    other_non_current_assets = Column(Float(20), doc="其他非流动资产(元)")
    total_non_current_assets = Column(Float(20), doc="非流动资产合计(元)")
    total_assets = Column(Float(20), doc="资产总计(元)")
    shortterm_loan = Column(Float(20), doc="短期借款(元)")
    borrowing_from_centralbank = Column(Float(20), doc="向中央银行借款(元)")
    deposit_in_interbank = Column(Float(20), doc="吸收存款及同业存放(元)")
    borrowing_capital = Column(Float(20), doc="拆入资金(元)")
    trading_liability = Column(Float(20), doc="交易性金融负债(元)")
    notes_payable = Column(Float(20), doc="应付票据(元)")
    accounts_payable = Column(Float(20), doc="应付账款(元)")
    advance_peceipts = Column(Float(20), doc="预收款项(元)")
    sold_buyback_secu_proceeds = Column(Float(20), doc="卖出回购金融资产款(元)")
    commission_payable = Column(Float(20), doc="应付手续费及佣金(元)")
    salaries_payable = Column(Float(20), doc="应付职工薪酬(元)")
    taxs_payable = Column(Float(20), doc="应交税费(元)")
    interest_payable = Column(Float(20), doc="应付利息(元)")
    dividend_payable = Column(Float(20), doc="应付股利(元)")
    other_payable = Column(Float(20), doc="其他应付款(元)")
    reinsurance_payables = Column(Float(20), doc="应付分保账款(元)")
    insurance_contract_reserves = Column(Float(20), doc="保险合同准备金(元)")
    proxy_secu_proceeds = Column(Float(20), doc="代理买卖证券款(元)")
    receivings_from_vicariously_sold_securities = Column(Float(20), doc="代理承销证券款(元)")
    non_current_liability_in_one_year = Column(Float(20), doc="年份")
    other_current_liability = Column(Float(20), doc="其他流动负债(元)")
    total_current_liability = Column(Float(20), doc="流动负债合计(元)")
    longterm_loan = Column(Float(20), doc="长期借款(元)")
    bonds_payable = Column(Float(20), doc="应付债券(元)")
    longterm_account_payable = Column(Float(20), doc="长期应付款(元)")
    specific_account_payable = Column(Float(20), doc="专项应付款(元)")
    estimate_liability = Column(Float(20), doc="预计负债(元)")
    deferred_tax_liability = Column(Float(20), doc="递延所得税负债(元)")
    other_non_current_liability = Column(Float(20), doc="其他非流动负债(元)")
    total_non_current_liability = Column(Float(20), doc="非流动负债合计(元)")
    total_liability = Column(Float(20), doc="负债合计(元)")
    paidin_capital = Column(Float(20), doc="实收资本(或股本)(元)")
    capital_reserve_fund = Column(Float(20), doc="资本公积(元)")
    treasury_stock = Column(Float(20), doc="减:库存股(元)")
    specific_reserves = Column(Float(20), doc="专项储备(元)")
    surplus_reserve_fund = Column(Float(20), doc="盈余公积(元)")
    ordinary_risk_reserve_fund = Column(Float(20), doc="一般风险准备(元)")
    retained_profit = Column(Float(20), doc="未分配利润(元)")
    foreign_currency_report_conv_diff = Column(Float(20), doc="外币报表折算差额(元)")
    equities_parent_company_owners = Column(Float(20), doc="归属于母公司股东权益合计(元)")
    minority_interests = Column(Float(20), doc="少数股东权益(元)")
    total_owner_equities = Column(Float(20), doc="股东权益合计(元)")
    total_sheet_owner_equities = Column(Float(20), doc="负债和股东权益合计")

# class CashFlowStatement(Base):
    """
    现金流表
    """

    # __tablename__ = 'cash_flow_statement'
    # __table_args__ = (
    #     Index('idx_day_code', 'day', 'code', unique=True),
    # )

    # id = Column(Integer, primary_key=True)
    # code = Column(String(12), nullable=False, doc="股票代码(带后缀: .XSHE/.XSHG)")

    # day = Column(Date, nullable=False, server_default=text("'0000-00-00'"), doc="日期")

    # pubDate = Column(Date, nullable=False, server_default=text("'0000-00-00'"))
    # statDate = Column(Date, nullable=False, server_default=text("'0000-00-00'"))
    # periodStart = Column(Date, nullable=False, server_default=text("'0000-00-00'"), doc="两次报告之间的日期范围:start date")
    # periodEnd = Column(Date, nullable=False, server_default=text("'0000-00-00'"), doc="两次报告之间的日期范围:end date")
    # reportId = Column(Integer, nullable=False, server_default=text("'0'"))
    goods_sale_and_service_render_cash = Column(Float(20), doc="销售商品、提供劳务收到的现金(元)")
    net_deposit_increase = Column(Float(20), doc="客户存款和同业存放款项净增加额(元)")
    net_borrowing_from_central_bank = Column(Float(20), doc="向中央银行借款净增加额(元)")
    net_borrowing_from_finance_co = Column(Float(20), doc="向其他金融机构拆入资金净增加额(元)")
    net_original_insurance_cash = Column(Float(20), doc="收到原保险合同保费取得的现金(元)")
    net_cash_received_from_reinsurance_business = Column(Float(20), doc="收到再保险业务现金净额(元)")
    net_insurer_deposit_investment = Column(Float(20), doc="保户储金及投资款净增加额(元)")
    net_deal_trading_assets = Column(Float(20), doc="交易性金融资产(元)")
    interest_and_commission_cashin = Column(Float(20), doc="收取利息、手续费及佣金的现金(元)")
    net_increase_in_placements = Column(Float(20), doc="拆入资金净增加额(元)")
    net_buyback = Column(Float(20), doc="回购业务资金净增加额(元)")
    tax_levy_refund = Column(Float(20), doc="收到的税费返还(元)")
    other_cashin_related_operate = Column(Float(20), doc="收到其他与经营活动有关的现金(元)")
    subtotal_operate_cash_inflow = Column(Float(20), doc="经营活动现金流入小计(元)")
    goods_and_services_cash_paid = Column(Float(20), doc="购买商品、接受劳务支付的现金(元)")
    net_loan_and_advance_increase = Column(Float(20), doc="客户贷款及垫款净增加额(元)")
    net_deposit_in_cb_and_ib = Column(Float(20), doc="存放中央银行和同业款项净增加额(元)")
    original_compensation_paid = Column(Float(20), doc="支付原保险合同赔付款项的现金(元)")
    handling_charges_and_commission = Column(Float(20), doc="支付利息、手续费及佣金的现金(元)")
    policy_dividend_cash_paid = Column(Float(20), doc="支付保单红利的现金(元)")
    staff_behalf_paid = Column(Float(20), doc="支付给职工以及为职工支付的现金(元)")
    tax_payments = Column(Float(20), doc="支付的各项税费(元)")
    other_operate_cash_paid = Column(Float(20), doc="支付其他与经营活动有关的现金(元)")
    subtotal_operate_cash_outflow = Column(Float(20), doc="经营活动现金流出小计(元)")
    net_operate_cash_flow = Column(Float(20), doc="经营活动产生的现金流量净额(元)")
    invest_withdrawal_cash = Column(Float(20), doc="收回投资收到的现金(元)")
    invest_proceeds = Column(Float(20), doc="取得投资收益收到的现金(元)")
    fix_intan_other_asset_dispo_cash = Column(Float(20), doc="处置固定资产、无形资产和其他长期资产收回的现金净额(元)")
    net_cash_deal_subcompany = Column(Float(20), doc="处置子公司及其他营业单位收到的现金净额(元)")
    other_cash_from_invest_act = Column(Float(20), doc="收到其他与投资活动有关的现金(元)")
    subtotal_invest_cash_inflow = Column(Float(20), doc="投资活动现金流入小计(元)")
    fix_intan_other_asset_acqui_cash = Column(Float(20), doc="购建固定资产、无形资产和其他长期资产支付的现金(元)")
    invest_cash_paid = Column(Float(20), doc="投资支付的现金(元)")
    impawned_loan_net_increase = Column(Float(20), doc="质押贷款净增加额(元)")
    net_cash_from_sub_company = Column(Float(20), doc="取得子公司及其他营业单位支付的现金净额(元)")
    other_cash_to_invest_act = Column(Float(20), doc="支付其他与投资活动有关的现金(元)")
    subtotal_invest_cash_outflow = Column(Float(20), doc="投资活动现金流出小计(元)")
    net_invest_cash_flow = Column(Float(20), doc="投资活动产生的现金流量净额(元)")
    cash_from_invest = Column(Float(20), doc="吸收投资收到的现金(元)")
    cash_from_mino_s_invest_sub = Column(Float(20), doc="其中:子公司吸收少数股东投资收到的现金(元)")
    cash_from_borrowing = Column(Float(20), doc="取得借款收到的现金(元)")
    cash_from_bonds_issue = Column(Float(20), doc="发行债券收到的现金(元)")
    other_finance_act_cash = Column(Float(20), doc="收到其他与筹资活动有关的现金(元)")
    subtotal_finance_cash_inflow = Column(Float(20), doc="筹资活动现金流入小计(元)")
    borrowing_repayment = Column(Float(20), doc="偿还债务支付的现金(元)")
    dividend_interest_payment = Column(Float(20), doc="分配股利、利润或偿付利息支付的现金(元)")
    proceeds_from_sub_to_mino_s = Column(Float(20), doc="其中:子公司支付给少数股东的股利、利润(元)")
    other_finance_act_payment = Column(Float(20), doc="支付其他与筹资活动有关的现金(元)")
    subtotal_finance_cash_outflow = Column(Float(20), doc="筹资活动现金流出小计(元)")
    net_finance_cash_flow = Column(Float(20), doc="筹资活动产生的现金流量净额(元)")
    exchange_rate_change_effect = Column(Float(20), doc="四、汇率变动对现金及现金等价物的影响")
    cash_equivalent_increase = Column(Float(20), doc="五、现金及现金等价物净增加额")
    cash_equivalents_at_beginning = Column(Float(20), doc="加:期初现金及现金等价物余额(元)")
    cash_and_equivalents_at_end = Column(Float(20), doc="期末现金及现金等价物余额(元)")


# class IncomeStatement(Base):
    """
    利润表
    """

    # __tablename__ = 'income_statement'
    # __table_args__ = (
    #     Index('idx_day_code', 'day', 'code', unique=True),
    # )

    # id = Column(Integer, primary_key=True)
    # code = Column(String(12), nullable=False, doc="股票代码(带后缀: .XSHE/.XSHG)")

    # day = Column(Date, nullable=False, server_default=text("'0000-00-00'"), doc="日期")

    # pubDate = Column(Date, nullable=False, server_default=text("'0000-00-00'"))
    # statDate = Column(Date, nullable=False, server_default=text("'0000-00-00'"))
    # periodStart = Column(Date, nullable=False, server_default=text("'0000-00-00'"), doc="两次报告之间的日期范围:start date")
    # periodEnd = Column(Date, nullable=False, server_default=text("'0000-00-00'"), doc="两次报告之间的日期范围:end date")
    # reportId = Column(Integer, nullable=False, server_default=text("'0'"))
    total_operating_revenue = Column(Float(20), doc="营业总收入(元)")
    operating_revenue = Column(Float(20), doc="营业收入(元)")
    interest_income = Column(Float(20), doc="利息收入(元)")
    premiums_earned = Column(Float(20), doc="已赚保费(元)")
    commission_income = Column(Float(20), doc="手续费及佣金收入(元)")
    total_operating_cost = Column(Float(20), doc="营业成本(元)")
    operating_cost = Column(Float(20), doc="营业成本(元)")
    interest_expense = Column(Float(20), doc="利息支出(元)")
    commission_expense = Column(Float(20), doc="手续费及佣金支出(元)")
    refunded_premiums = Column(Float(20), doc="退保金(元)")
    net_pay_insurance_claims = Column(Float(20), doc="赔付支出净额(元)")
    withdraw_insurance_contract_reserve = Column(Float(20), doc="提取保险合同准备金净额(元)")
    policy_dividend_payout = Column(Float(20), doc="保单红利支出(元)")
    reinsurance_cost = Column(Float(20), doc="分保费用(元)")
    operating_tax_surcharges = Column(Float(20), doc="营业税金及附加(元)")
    sale_expense = Column(Float(20), doc="销售费用(元)")
    administration_expense = Column(Float(20), doc="管理费用(元)")
    financial_expense = Column(Float(20), doc="财务费用(元)")
    asset_impairment_loss = Column(Float(20), doc="资产减值损失(元)")
    fair_value_variable_income = Column(Float(20), doc="公允价值变动收益(元)")
    investment_income = Column(Float(20), doc="投资收益(元)")
    invest_income_associates = Column(Float(20), doc="对联营企业和合营企业的投资收益(元)")
    exchange_income = Column(Float(20), doc="汇兑收益(元)")
    operating_profit = Column(Float(20), doc="营业利润(元)")
    non_operating_revenue = Column(Float(20), doc="营业外收入(元)")
    non_operating_expense = Column(Float(20), doc="营业外支出(元)")
    disposal_loss_non_current_liability = Column(Float(20), doc="非流动资产处置净损失(元)")
    total_profit = Column(Float(20), doc="利润总额(元)")
    income_tax_expense = Column(Float(20), doc="所得税费用(元)")
    net_profit = Column(Float(20), doc="净利润(元)")
    np_parent_company_owners = Column(Float(20), doc="归属于母公司股东的净利润(元)")
    minority_profit = Column(Float(20), doc="少数股东损益(元)")
    basic_eps = Column(Float(20), doc="基本每股收益(元)")
    diluted_eps = Column(Float(20), doc="稀释每股收益(元)")
    other_composite_income = Column(Float(20), doc="其他综合收益(元)")
    total_composite_income = Column(Float(20), doc="综合收益总额(元)")
    ci_parent_company_owners = Column(Float(20), doc="归属于母公司所有者的综合收益总额(元)")
    ci_minority_owners = Column(Float(20), doc="归属于少数股东的综合收益总额(元)")
    # compId = Column(String(16), nullable=False, unique=True, server_default=text("''"))


# class StockValuation(Base):
    """
    市值表
    """
    # __tablename__ = 'stock_valuation'
    # __table_args__ = (
    #     Index('idx_statDate_code', 'statDate', 'code', unique=True),
    #     Index('idx_day_code', 'day', 'code', unique=True)
    # )

    # id = Column(Integer, primary_key=True)
    # code = Column(String(12), nullable=False, doc="股票代码(带后缀: .XSHE/.XSHG)")
    year = Column(String(4), nullable=False, doc="年份")
    type = Column(String(64), nullable=False, doc="Q1,S1,Q3,A")
    # pubDate = Column(Date, nullable=False, server_default=text("'0000-00-00'"))
    # statDate = Column(Date, nullable=False, server_default=text("'0000-00-00'"))
    # periodStart = Column(Date, nullable=False, server_default=text("'0000-00-00'"), doc="两次报告之间的日期范围:start date")
    # periodEnd = Column(Date, nullable=False, server_default=text("'0000-00-00'"), doc="两次报告之间的日期范围:end date")
    # reportId = Column(Integer, nullable=False, server_default=text("'0'"))
    pe_ratio = Column(Float(20), doc='市盈率')
    turnover_ratio = Column(Float(20), doc="换手率")
    pb_ratio = Column(Float(20), doc="市净率")
    ps_ratio = Column(Float(20), doc="市销率")
    pcf_ratio = Column(Float(20), doc="市现率")
    capitalization = Column(Float(20), doc="总股本(万股)")
    market_cap = Column(Float(20), doc="总市值(亿元)")
    circulating_cap = Column(Float(20), doc="流通股本(万股)")
    circulating_market_cap = Column(Float(20), doc="总市值(亿元)")
    day = Column(Date, nullable=False, doc="日期")
    # compId = Column(String(16), nullable=False, unique=True, server_default=text("''"))
    pe_ratio_lyr = Column(Float(20), doc="市盈率LYR")


# class FinancialIndicator(Base):
    """
    财务指标表
    """

    # __tablename__ = 'financial_indicator'

    # id = Column(Integer, primary_key=True, doc="id")
    # code = Column(String(12), nullable=False, doc="股票代码(带后缀: .XSHE/.XSHG)")
    # day = Column(Date, nullable=False, server_default=text("'0000-00-00'"), doc="日期")
    # pubDate = Column(Date, nullable=False, server_default=text("'0000-00-00'"))
    # statDate = Column(Date, nullable=False, server_default=text("'0000-00-00'"))
    # periodStart = Column(Date, nullable=False, server_default=text("'0000-00-00'"), doc="两次报告之间的日期范围:start date")
    # periodEnd = Column(Date, nullable=False, server_default=text("'0000-00-00'"), doc="两次报告之间的日期范围:end date")
    # reportId = Column(Integer, nullable=False, server_default=text("'0'"))
    eps = Column(Float(20), doc="每股收益EPS(元)")
    adjusted_profit = Column(Float(20), doc="扣除非经常损益后的净利润(元)")
    # operating_profit = Column(Float(20), doc="经营活动净收益(元)")
    value_change_profit = Column(Float(20), doc="价值变动净收益(元)")
    roe = Column(Float(20), doc="净资产收益率ROE(%)")
    inc_return = Column(Float(10), doc="净资产收益率(扣除非经常损益)(%)")
    roa = Column(Float(10), doc="总资产净利率ROA(%)")
    net_profit_margin = Column(Float(10), doc="销售净利率(%)")
    gross_profit_margin = Column(Float(10), doc="销售毛利率(%)")
    expense_to_total_revenue = Column(Float(10), doc="营业总成本/营业总收入(%)")
    operation_profit_to_total_revenue = Column(Float(10), doc="营业利润/营业总收入(%)")
    net_profit_to_total_revenue = Column(Float(10), doc="净利润/营业总收入(%)")
    operating_expense_to_total_revenue = Column(Float(10), doc="营业费用/营业总收入(%)")
    ga_expense_to_total_revenue = Column(Float(10), doc="管理费用/营业总收入(%)")
    financing_expense_to_total_revenue = Column(Float(10), doc="财务费用/营业总收入(%)")
    operating_profit_to_profit = Column(Float(10), doc="经营活动净收益/利润总额(%)")
    invesment_profit_to_profit = Column(Float(10), doc="价值变动净收益/利润总额(%)")
    adjusted_profit_to_profit = Column(Float(10), doc="扣除非经常损益后的净利润/净利润(%)")
    goods_sale_and_service_to_revenue = Column(Float(10), doc="销售商品提供劳务收到的现金/营业收入(%)")
    ocf_to_revenue = Column(Float(10), doc="经营活动产生的现金流量净额/营业收入(%)")
    ocf_to_operating_profit = Column(Float(10), doc="经营活动产生的现金流量净额/经营活动净收益(%)")
    inc_total_revenue_year_on_year = Column(Float(10), doc="营业总收入同比增长率(%)")
    inc_total_revenue_annual = Column(Float(10), doc="营业总收入环比增长率(%)")
    inc_revenue_year_on_year = Column(Float(10), doc="营业收入同比增长率(%)")
    inc_revenue_annual = Column(Float(10), doc="营业收入环比增长率(%)")
    inc_operation_profit_year_on_year = Column(Float(10), doc="营业利润同比增长率(%)")
    inc_operation_profit_annual = Column(Float(10), doc="营业利润环比增长率(%)")
    inc_net_profit_year_on_year = Column(Float(10), doc="净利润同比增长率(%)")
    inc_net_profit_annual = Column(Float(10), doc="净利润环比增长率(%)")
    inc_net_profit_to_shareholders_year_on_year = Column(Float(10), doc="归属母公司股东的净利润同比增长率(%)")
    inc_net_profit_to_shareholders_annual = Column(Float(10), doc="归属母公司股东的净利润环比增长率(%)")
    # status = Column(Integer, nullable=False, server_default=text("'0'"))
    # addTime = Column(DateTime, nullable=False, server_default=text("'0000-00-00 00:00:00'"))
    # modTime = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


engine = create_engine('sqlite:////Users/jiangtianyu/ziplinedata/sqlitedb/data.db', echo=True)
Base.metadata.create_all(engine)
