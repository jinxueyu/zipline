from multiprocessing import Process
import os
from algorithm import RealtimeAlgorithm
from bardata import RealtimeBarData

ALGO_PATH = '/Users/limeng/workspace/github/zipline/zipline/examples/realtime'


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
            ra = RealtimeAlgorithm(script=algotext, algo_filename=file)
            self.algos.add(ra)
          except:
            print("A ERROR!")
        print('Algo Reactor loaded algo:{}'.format(file))
    for algo in self.algos:
      algo.initialize()

  def run(self):
    print('AlgoProcess start')
    self.load_algos()
    while True:
      quote_data = self._quote_queue.get(True)
      bar_data = RealtimeBarData(minute_bar=quote_data)
      for algo in self.algos:
          try:
            if algo.symbol == bar_data.get_symbol():
                algo.handle_data(bar_data)
          except Exception as error:
              print(error)