from queue import Queue
import threading

def basic_worker(queue):
    while True:
        item = queue.get()
        # do_work(item)
        print(item)
        queue.task_done()
def basic():
    # http://docs.python.org/library/queue.html
    queue = Queue()
    for i in range(3):
         t = threading.Thread(target=basic_worker,args=(queue,))
         t.daemon = True
         t.start()
    for item in range(4):
        queue.put(item)
    queue.join()       # block until all tasks are done
    print('got here')

basic()