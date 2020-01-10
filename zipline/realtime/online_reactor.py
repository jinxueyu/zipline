# -*- coding: utf-8 -*-
import asyncio,time,os
from nats.aio.client import Client as NATS
from multiprocessing import Queue
from algo_process import AlgoProcess
from order_process import OrderProcess

def order(data):
    order_queue.put(data)

async def run(loop):
    nc = NATS()

    await nc.connect("nats://100.116.1.62:4222", loop=loop)

    async def message_handler(msg):
        subject = msg.subject
        reply = msg.reply
        data = msg.data.decode()
        print('Process_QuoteSub({}) receive quote: {}'.format(os.getpid(),data))
        quote_queue.put(data)

    sid = await nc.subscribe("1_min_bar", cb=message_handler)

quote_queue = Queue()
order_queue = Queue()

if __name__=='__main__':
    # 启动策略运行进程
    algo_process = AlgoProcess(quote_queue, order_queue)
    algo_process.start()

    # 启动下单进程
    order_process = OrderProcess(order_queue)
    order_process.start()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop))
    print('Process_QuoteSub({}) ready'.format(os.getpid()))
    try:
        loop.run_forever()
    finally:
        loop.close()