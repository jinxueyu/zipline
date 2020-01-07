select to_char(stk.tradedate,'YYYY-MM-DD') as "date",
    nvl(open,0) as "open",
    nvl(high,0) as "high",
    nvl(low,0) as "low",
    nvl(new,0) as "close",
    nvl(tvol,0) as "volume",
    0.0 as "dividend",
    1.0 as "split"
    from (select tradedate,open,high,low,new,tvol
          from outuser.trad_sk_daily_jc
          where securitycode='${code}'
              and eisdel=0
              and tradedate>=to_date('2017-01-01','YYYY-MM-DD')
              and tradedate<=to_date('2019-12-31','YYYY-MM-DD')) stk
    join (select tradedate
          from outuser.trad_td_tdate
          where eisdel=0
              and trademarketcode='069001001'
              and tradedate>='20170101'
              and tradedate<='20191231' ) all_trade_date
    on to_char(stk.tradedate,'YYYYMMDD')=all_trade_date.tradedate
    order by stk.tradedate;