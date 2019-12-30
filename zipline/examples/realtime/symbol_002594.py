'''
网格策略
客户号：001
股票代码：002594.sz
基准价格：47.00
档位价格：5%
每次交易：100股
'''
def initialize(context):
  context.client_id = "001"
  context.symbol = "002594.sz"
  context.base_price = 47.00
  context.ratio = 0.05
  context.qty_per_match = 100
  context.position = 0


def handle_data(context, data):
  last_price = data.current(context,
                            ["symbol", "open", "high", "low", "close"])["close"]
  buy_price = round(context.base_price * (1 - context.ratio), 2)
  sell_price = round(context.base_price * (1 + context.ratio), 2)
  if last_price <= buy_price:
    context.position += context.qty_per_match
    context.base_price = last_price
    print('Client[{}] buy[{}] qty[{}] at price[{}], position[{}]'.format(
        context.client_id, context.symbol, context.qty_per_match, last_price, context.position))
  elif last_price >= sell_price:
    if context.position >= context.qty_per_match:
      context.position -= context.qty_per_match
      context.base_price = last_price
      print('Client[{}] sell[{}] qty[{}] at price[{}], position[{}]'.format(
          context.client_id, context.symbol, context.qty_per_match, last_price, context.position))
