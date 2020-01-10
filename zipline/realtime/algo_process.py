from multiprocessing import Process
import os
from algorithm import RealtimeAlgorithm
from bardata import RealtimeBarData

ALGO_PATH = '/Users/limeng/workspace/github/zipline/zipline/examples/realtime/one'


class AlgoProcess(Process):
  def __init__(self, quote_queue, order_queue):
    super().__init__()
    self._quote_queue = quote_queue
    self._order_queue = order_queue
    self.algos = set()

  def load_algos(self):
    # 读取策略文件
    for file in os.listdir(ALGO_PATH):
      if file.endswith(".py"):
        with open(os.path.join(ALGO_PATH, file), 'r') as f:
          algotext = f.read()
          try:

            def order_call_back(order_data):
              self._order_queue.put(order_data)

            ra = RealtimeAlgorithm(
                script=algotext,
                algo_filename=file,
                order_callback=order_call_back)
            self.algos.add(ra)
          except:
            print("A ERROR!")
        print('Process_Algo({}) loaded algo:{}'.format(os.getpid(), file))
    for algo in self.algos:
      algo.initialize()

  def run(self):
    print('Process_Algo({}) ready'.format(os.getpid()))
    self.load_algos()
    while True:
      quote_data = self._quote_queue.get(True)
      bar_data = RealtimeBarData(minute_bar=quote_data)
      for algo in self.algos:
        try:
          if algo.symbol == bar_data.get_symbol():
            print('Process_Algo({}) match stock symbol:{}'.format(
                os.getpid(), algo.symbol))
            algo.handle_data(bar_data)
        except Exception as error:
          print(error)
