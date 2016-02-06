from threads.abstract_thread import AbstractThread
from queue import Queue
from archiver.snapshot_archiver import SnapshotArchiver
from sentinels import _sentinelCamera
from pprint import pprint

class ArchiverThreadManager(AbstractThread):
    
    '''
    expects already setup Mic
    '''
    def run(self, archiver: SnapshotArchiver, queue: Queue, pictures_directory='./pictures/'):
        busy = False
        while self._running:
            queue_data = queue.get()
            pprint(queue_data is _sentinelCamera)
            if queue_data is _sentinelCamera and busy == False:
                busy = True
                archiver.archivePictures(pictures_directory)
                busy = False
