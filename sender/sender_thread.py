from threads.abstract_thread import AbstractThread
from queue import Queue
from sentinels import Sentinel


class SenderThreadManager(AbstractThread):
    
    def __init__(self):
        AbstractThread.__init__(self)
    '''
    '''
    def run(self, mailer, queue: Queue):
        while self._running:
            queue_data = queue.get()
            if queue_data.getAction() == Sentinel.senderAction:
                print('sending email')
                archive_to_send = queue.get_meta()
                print(archive_to_send)
                mailer.sendLastArchive(archive_to_send)