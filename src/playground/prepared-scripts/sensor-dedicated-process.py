from multiprocessing import Process, Queue
import time
from random import randint

def emptyQueue(queue):
    items = []
    while not queue.empty():
        item = queue.get_nowait()
        if item:
            items.append(item)
    return items

class Sensor(Process):

    def __init__(self, queue, interval=1):
        Process.__init__(self)
        self.queue = queue
        self.interval = interval

    def run(self):
        self._loop()

    def _loop(self):
        time.sleep(self.interval)
        value = self._measure()
        if self.queue.full():
            print('[Sensor] _loop(): queue full => deleting item')
            self.queue.get_nowait()
        self.queue.put(value)
        self._loop()

    def _measure(self):
        return randint(0, 9)

class Application(object):

    def __init__(self):
        self._initialize()

    def _initialize(self):
        queue = Queue(10)
        Sensor(queue).start()
        self._loop(queue)

    def _loop(self, queue):
        try:
            while True:
                print('.')
                time.sleep(3)
                results = emptyQueue(queue)
                if results:
                    print('results: {}'.format(results))
        except KeyboardInterrupt:
            print('interrupted!')

    @staticmethod
    def main():
        Application()

if __name__ == '__main__':
    Application.main()
