import queue, threading, socket, json

class InMemoryIPC:
    def __init__(self):
        self.queues = {}
        self.lock = threading.Lock()
    def get_queue(self, name):
        with self.lock:
            if name not in self.queues:
                self.queues[name] = queue.Queue()
            return self.queues[name]
    def send(self, target, msg):
        self.get_queue(target).put(msg)
    def recv(self, target, timeout=1.0):
        try:
            return self.get_queue(target).get(timeout=timeout)
        except queue.Empty:
            return None
