from threading import Thread
from queue import Queue
from core.helper.XMLParser import XMLParser

queue = Queue(150)


class ProducerThread(Thread):

    def __init__(self, element_list):
        super(ProducerThread, self).__init__()
        self.element_list = element_list

    def run(self):
        global queue
        while self.element_list:
            each_item = self.element_list.pop()
            queue.put(each_item)


class ConsumerThread(Thread):
    @staticmethod
    def process(each_item):
        XMLParser(each_item).start()

    def run(self):
        global queue
        while not queue.empty():
            each_item = queue.get()
            self.process(each_item)
            queue.task_done()
