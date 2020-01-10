from multiprocessing import Process
import os

class OrderProcess(Process):
    def __init__(self,order_queue):
        super().__init__()
        self._order_queue = order_queue

    def run(self):
        print('Process_Order({}) Ready'.format(os.getpid()))
        while True:
            order_data = self._order_queue.get(True)
            print('Process_Order({}) receive msg: {}'.format(os.getpid(),order_data))