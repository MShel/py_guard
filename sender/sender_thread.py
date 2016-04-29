from queue import Queue

from sentinels import Sentinel
from threads.abstract_thread import AbstractThread


class SenderThreadManager(AbstractThread):
    def __init__(self):
        AbstractThread.__init__(self)

    '''
    '''

    def run(self, mailer, queue: Queue):
        while self._running:
            queue_data = queue.get()
            if queue_data.get_action() == Sentinel.senderAction:
                print('sending email')
                archive_to_send = queue_data.get_meta()
                print(archive_to_send)
                mailer.send_all()
