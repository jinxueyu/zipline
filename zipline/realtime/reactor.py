import os
import sys
from zipline.realtime.algorithm import RealtimeAlgorithm
from zipline.realtime.bardata import RealtimeBarData
import asyncio
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers
import logging
import time
from concurrent.futures import ThreadPoolExecutor


class AlgorithmReactor(object):
  def __init__(self, algo_path=None, mq_url=None):
    self._algo_path = algo_path
    self._mq_url = mq_url
    self._algos = set()
    self._executor = ThreadPoolExecutor(max_workers=10)
    self._tasks = set()

  def initial(self):
    # 读取策略文件
    for file in os.listdir(self._algo_path):
      if file.endswith(".py"):
        with open(os.path.join(self._algo_path, file), 'r') as f:
          algotext = f.read()
          try:
            # i = 0
            # while i < 100:
            ra = RealtimeAlgorithm(script=algotext, algo_filename=file)
            self._algos.add(ra)
          #   i = i + 1
          except:
            print("A ERROR!")
        print('Algo Reactor loaded algo:{}'.format(file))
    # print(len(self._algos))
    for algo in self._algos:
      algo.initialize()

  async def message_handler(self, msg):
    subject = msg.subject
    reply = msg.reply
    data = msg.data.decode()
    logging.info("'{subject}':{data}".format(subject=subject, data=data))

    for task in self._tasks:
      if not task.done():
        if not task.cancel():
          print("task has not done, ")
    self._tasks.clear()

    # print(time.time())
    last_time = time.time()
    # print(data)
    bar_data = RealtimeBarData(minute_bar=data)
    for algo in self._algos:
      if algo.symbol == bar_data.get_symbol():
        algo.handle_data(bar_data)
        # task = self._executor.submit(algo.handle_data, (bar_data))
        # self._tasks.add(task)
      # algo.handle_data(data)
    # print(time.time())
    now = time.time() - last_time
    print('cost seconds:%.6f' % now)

  def start(self):
    # MQ连接和订阅
    async def run(loop):
      self._nc = NATS()

      await self._nc.connect(self._mq_url, loop=loop)
      # print("nats connected.")
      # print('Algo Reactor initialize successfully!')
      await self._nc.subscribe("1_min_bar", cb=self.message_handler)

    self._loop = asyncio.get_event_loop()
    asyncio.ensure_future(run(self._loop))
    self._loop.run_forever()
