from queue import Queue

from archiver.snapshot_archiver import SnapshotArchiver
from sentinels import Sentinel
from threads.abstract_thread import AbstractThread


class ArchiverThreadManager(AbstractThread):
    '''
    expects already setup Mic
    '''

    def run(self, archiver: SnapshotArchiver, queue: Queue, pictures_directory='./pictures/'):
        busy = False
        while self._running:
            queue_data = queue.get()
            if queue_data.get_action() == Sentinel.archiveAction and busy == False:
                busy = True
                archiver.archivePictures(pictures_directory)
                busy = False
