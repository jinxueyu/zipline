select to_char(tradedate,'YYYY-MM-DD') as "date",
    nvl(open,0) as "open",
    nvl(high,0) as "high",
    nvl(low,0) as "low",
    nvl(new,0) as "close",
    nvl(tvol,0) as "volume",
    0.0 as "dividend",
    1.0 as "split"
    from outuser.index_td_daily
    where securitycode='${code}'
        and eisdel=0
        and tradedate>=to_date('2010-01-01','YYYY-MM-DD')
        and tradedate<=to_date('2019-12-31','YYYY-MM-DD')
    order by tradedate;