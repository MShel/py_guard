from threads.abstract_thread import AbstractThread
from camera.camera import Camera 
from queue import Queue
from sentinels import Sentinel


class CameraThreadManager(AbstractThread):
    
    def __init__(self):
        AbstractThread.__init__(self)
        self.pictures_amount = 1
        self.taps_count = 2
        self.pictures_directory = './pictures/'
    
    '''
    expects already setup Camera
    taps_count amount of taps  before picture is taken
    pictures_amount amount of pictures before we will alert archiver
    '''
    def run(self, cam: Camera, queue: Queue, taps_count=None, pictures_amount=None, pictures_directory=None):
        if taps_count is None: taps_count = self.taps_count
        if pictures_amount is None: pictures_amount = self.pictures_amount
        if pictures_directory is None: pictures_directory = self.pictures_directory

        taps = 0
        
        while self._running:
            queue_data = queue.get()
            if queue_data.getAction == Sentinel.microphoneAction:
                taps += 1
                if taps == taps_count:
                    cam.takeNPictures(1, pictures_directory, pictures_amount)
                    taps = 0