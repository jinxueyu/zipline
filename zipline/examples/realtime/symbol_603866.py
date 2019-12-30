def initialize(context):
  context.client_id = "001"
  context.symbol = "603866.sh"
  context.base_price = 47.00
  context.ratio = 0.05
  context.qty_per_match = 100
  context.position = 0

def handle_data(context, data):
  last_price = data.current(context, ["symbol","open", "high", "low", "close"])["close"]
  print(last_price)
  if last_price <= context.base_price * (1 - context.ratio):
    print('Client:{} buy:{}, qty:{} at price:{}'.format(
        context.client_id, context.symbol, context.qty_per_match, last_price))
    context.position += context.qty_per_match
    context.base_price = last_price
  elif last_price >= context.base_price * (1 + context.ratio):
    if context.position >= context.qty_per_match:
      print('Client:{} sell:{} qty:{} at price:{}'.format(
          context.client_id, context.symbol, context.qty_per_match, last_price))
      context.position -= context.qty_per_match
      context.base_price = last_price
