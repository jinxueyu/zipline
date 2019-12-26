#!/bin/python
import sys
import json
import datetime

key_market_id = 'sh'
key_security_id = 'securityID'
key_timestamp = 'timestamp'
key_now_price = 'tradePrice'
key_vol = 'tradeVolume'
key_val = 'totalValueTraded'


def read_mapper_output(file):
    for line in file:
        json_message = json.loads(line)
        yield json_message


td = datetime.timedelta(hours=8)
tz = datetime.timezone(td)


def get_bar_date_time_sh(timestamp):
    try:
        timestamp = timestamp // 1000
        plus_timestamp = timestamp + 60
        dt_obj = datetime.datetime.fromtimestamp(plus_timestamp, tz)
        dt_str = dt_obj.strftime('%Y%m%d%H%M')
        d = dt_str[0:8]
        t = dt_str[8:12]
        return int(d), int(t)
    except:
        return None, None


def format_output_data(market_id, security_id, bar_date, bar_time, open, high, low, close, vol, val):
    result_dic = {'market_id': market_id,
                  'security_id': security_id,
                  'bar_date': bar_date,
                  'bar_time': bar_time,
                  'open': open,
                  'high': high,
                  'low': low,
                  'close': close,
                  'vol': vol,
                  'val': val}
    json_str = json.dumps(result_dic)
    return json_str


def main():
    data = read_mapper_output(sys.stdin)
    # 定义 cache_dic={security_id:[date_yyyymmdd,time_hhmm,open,high,low,close,begin_vol,begin_val]}
    cache_dic = {}
    for jsonObj in data:
        # 通过代码判断，如果数据不是指数、股票就放弃
        security_id = jsonObj.get(key_security_id)
        if security_id is None or len(security_id) != 6 or security_id[0:1] != '6':
            continue
        # 通过时间判断
        # 正常处理：
        #  新bar_date进来，不发消息，删除旧信息，保存新信息。
        #  相同bar_time进来，只更新高，低，收
        #  新的bar_time进来，高开低收立刻确定，交易量交易笔数用当前减去缓存的begin_vxl，生成bar发出去，新bar_time数据存起来
        # 异常处理：
        #  分钟bar 必定出现在[9:31,11:30],[13:01,15:00],11：30和15：00 过来的最后一个bar 要和前面的数据一起统计高开低收
        #  bar_time [0:00,9:30] 都不要
        #  bar_time [9:31,11:29] 正常处理
        #  bar_time 11:30 当11:31进入的时候，把11:31的当前价算入11:30的高低收和交易量中，仅仅保存begin_vxl
        #  bar_time [11:32,13:00] 都不要
        #  bar_time [13:01,14:59] 正常处理
        #  bar_time 15:00 当15:01进入的时候，把15:01的当前价算入15:00的高低收和交易量中，清空数据。后面的15:01进来就不要了
        #  bar_time [15:02,23:59] 都不要
        # 盘尾集合竞价：
        #  上海 直接14:57 然后就是 15:00
        #  深圳 直接14:57 然后就是 15:00
        bar_date, bar_time = get_bar_date_time_sh(jsonObj.get(key_timestamp))
        if bar_date is None or bar_time is None: continue
        now_price = jsonObj.get(key_now_price)
        if now_price is None: continue
        now_vol = jsonObj.get(key_vol)
        if now_vol is None: continue
        now_val = jsonObj.get(key_val)
        if now_val is None: continue
        old_data = cache_dic.get(security_id)
        if bar_time <= 930 or 1132 <= bar_time <= 1300 or 1502 <= bar_time:
            continue
        elif 931 <= bar_time <= 1130 or 1302 <= bar_time <= 1500:
            if old_data is None or old_data[0] is None or old_data[0] != bar_date:
                cache_dic[security_id] = [bar_date, bar_time, now_price, now_price, now_price, now_price, now_vol,
                                          now_val]
            else:
                if old_data[1] == bar_time:
                    if now_price > old_data[3]: old_data[3] = now_price
                    if now_price < old_data[4]: old_data[4] = now_price
                    old_data[5] = now_price
                else:

                    del_vol = now_vol - old_data[6]
                    del_val = now_val - old_data[7]
                    json_str = format_output_data(key_market_id, security_id, old_data[0], old_data[1], old_data[2],
                                                  old_data[3], old_data[4], old_data[5], del_vol, del_val)
                    print(json_str)
                    cache_dic[security_id] = [bar_date, bar_time, now_price, now_price, now_price, now_price, now_vol,
                                              now_val]
        elif bar_time == 1131 or bar_time == 1501:
            if old_data is None or old_data[0] is None:
                continue
            else:
                if now_price > old_data[3]: old_data[3] = now_price
                if now_price < old_data[4]: old_data[4] = now_price
                old_data[5] = now_price
                del_vol = now_vol - old_data[6]
                del_val = now_val - old_data[7]
                json_str = format_output_data(key_market_id, security_id, old_data[0], old_data[1], old_data[2],
                                              old_data[3], old_data[4], old_data[5], del_vol, del_val)
                print(json_str)
                cache_dic[security_id] = [None, None, None, None, None, None, now_vol, now_val]
        elif bar_time == 1301:
            if old_data is None:
                continue
            else:
                if old_data[0] is None:
                    cache_dic[security_id] = [bar_date, bar_time, now_price, now_price, now_price, now_price,
                                              old_data[6], old_data[7]]
                else:
                    if now_price > old_data[3]: old_data[3] = now_price
                    if now_price < old_data[4]: old_data[4] = now_price
                    old_data[5] = now_price


if __name__ == "__main__":
    main()
