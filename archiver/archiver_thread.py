from threads.abstract_thread import AbstractThread
from camera.camera import Camera 
from queue import Queue
from microphone.microphone import _sentinelMic
from datetime import datetime
import time
from archiver.snapshot_archiver import SnapshotArchiver
from camera.camera import _sentinelCamera
from pprint import pprint
_sentinel_archiver_to_emailer = object()

class ArchiverThreadManager(AbstractThread):
    
    '''
    expects already setup Mic
    '''
    def run(self, archiver: SnapshotArchiver, queue: Queue, pictures_directory='./pictures/'):
        busy = False
        while self._running:
            queue_data = queue.get()
            pprint(queue_data is _sentinelCamera)
            if queue_data is _sentinelCamera:
                busy = True
                pprint('worked')
                archive_name = archiver.archivePictures(pictures_directory)
                archiver.cleanPictures()
                _sentinel_archiver_to_emailer.archive_name = archive_name
                queue.put(_sentinel_archiver_to_emailer) 
                busy = False
