from threads.abstract_thread import AbstractThread
from camera.camera import Camera 
from queue import Queue
from pprint import pprint
from sentinels import _sentinelArchiver


class SenderThreadManager(AbstractThread):
    
    def __init__(self):
        AbstractThread.__init__(self)
    '''
    '''
    def run(self, mailer, queue: Queue):
        while self._running:
            queue_data = queue.get()
            if queue_data is _sentinelArchiver:
                mailer.send()