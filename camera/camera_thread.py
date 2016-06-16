from threads.abstract_thread import AbstractThread
from camera.camera import Camera 
from queue import Queue
from sentinels import Sentinel


class CameraThreadManager(AbstractThread):
    
    def __init__(self):
        AbstractThread.__init__(self)
        self.taps_count = 2

    '''
    expects already setup Camera
    taps_count amount of taps  before picture is taken
    pictures_amount amount of pictures before we will alert archiver
    '''
    def run(self, cam: Camera, queue: Queue, taps_count=None):
        if taps_count is None: taps_count = self.taps_count

        taps = 0
        
        while self._running:
            queue_data = queue.get()
            if queue_data.get_action() == Sentinel.microphoneAction:
                taps += 1
                if taps == taps_count:
                    cam.takeNPictures()
                    taps = 0