from queue import Queue

from archiver.snapshot_archiver import SnapshotArchiver
from sentinels import Sentinel
from threads.abstract_thread import AbstractThread


class ArchiverThreadManager(AbstractThread):
    '''
    expects already setup Mic
    '''

    def run(self, archiver: SnapshotArchiver, queue: Queue):
        busy = False
        while self._running:
            queue_data = queue.get()
            if queue_data.get_action() == Sentinel.archiveAction and busy is False:
                busy = True
                archiver.archivePictures()
                busy = False
