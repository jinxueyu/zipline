# -*- coding: utf-8 -*-
import os
import asyncio
import time
from nats.aio.client import Client as NATS
from nats.aio.errors import ErrConnectionClosed, ErrTimeout, ErrNoServers
from algorithm import RealtimeAlgorithm
from bardata import RealtimeBarData
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from pathos.multiprocessing import ProcessingPool
import multiprocessing

ALGO_PATH = '/Users/limeng/workspace/github/zipline/zipline/examples/realtime/one'
MQ_URL = 'nats://100.116.1.62:4222'

algos = set()
# executor = ProcessingPool()
executor = multiprocessing.Pool(processes=4)

# executor = ThreadPoolExecutor(100)
# executor = ProcessPoolExecutor(4)


def initial():
  # 读取策略文件
  for file in os.listdir(ALGO_PATH):
    if file.endswith(".py"):
      with open(os.path.join(ALGO_PATH, file), 'r') as f:
        algotext = f.read()
        index = 0
        while (index < 10):
          try:
            ra = RealtimeAlgorithm(script=algotext, algo_filename=file)
            algos.add(ra)
            index = index + 1
          except:
            print("A ERROR!")
      print('Algo Reactor loaded algo:{}'.format(file))
  for algo in algos:
    algo.initialize()

def test(i):
    print("test")

def handle_data(algo, bar_data):
  print("test")
  algo.handle_data(bar_data)


async def message_handler(msg):
  subject = msg.subject
  reply = msg.reply
  data = msg.data.decode()
  last_time = time.time()
  bar_data = RealtimeBarData(minute_bar=data)
  tasks = []
  for algo in algos:
    if algo.symbol == bar_data.get_symbol():
    #   print("iterate...")
    #   executor.amap(handle_data, algo, bar_data)
      executor.apply_async(algo.handle_data,(bar_data,))
    #   tasks.append(executor.submit(handle_data, algo, bar_data))
#   executor.close() # 关闭进程池，表示不能在往进程池中添加进程
#   executor.join() 

#   executor.close()
#   executor.join()
#   for future in as_completed(tasks):
    # print("done.")
#   executor.close()
#   executor.join()
  now = time.time() - last_time
  print('cost seconds:%.6f' % now)

async def run(loop):
  nc = NATS()

  await nc.connect(MQ_URL, loop=loop)
  # print("nats connected.")
  # print('Algo Reactor initialize successfully!')
  await nc.subscribe("1_min_bar", cb=message_handler)


if __name__ == '__main__':
  initial()
  loop = asyncio.get_event_loop()
  loop.run_until_complete(run(loop))
  try:
    loop.run_forever()
  finally:
    loop.close()
