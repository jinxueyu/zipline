from multiprocessing import Process

class OrderProcess(Process):
    def __init__(self,order_queue):
        super().__init__()
        self._order_queue = order_queue

    def run(self):
        print('OrderProcess start')
        while True:
            order_data = self._order_queue.get(True)
            print(order_data)