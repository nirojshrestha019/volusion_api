from core.config.paths import root_path
from core.config.paths import input_path
from core.config.paths import output_path
from core.helper.ProducerConsumerThread import ProducerThread
from core.helper.ProducerConsumerThread import ConsumerThread
from core.helper.XMLParser import XMLParser


class XmlProcess:
    def __init__(self, root_element, element="Products"):
        self.root_element = root_element
        self.element = element
        self.output_file = ""
        self.root_path = root_path
        self.input_path = input_path
        self.output_path = output_path
        self.element_list = list()

    def file_read(self):
        for element in self.root_element.iter(self.element):
            self.element_list.append(element)

    def processing(self):
        XMLParser.total_element = len(self.element_list)
        # total_element = len(self.element_list)
        p1 = ProducerThread(self.element_list)
        producer_thread_list = list()
        producer_thread_list.append(p1)
        consumer_thread_list = [ConsumerThread() for x in range(111)]
        for each_producer in producer_thread_list:
            each_producer.start()
        for each_consumer in consumer_thread_list:
            each_consumer.start()
        for each_producer in producer_thread_list:
            each_producer.join()
        for each_consumer in consumer_thread_list:
            each_consumer.join()

    def start(self):
        self.file_read()
        self.processing()
        XMLParser.output_csv()
