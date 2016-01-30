from threads.abstract_thread import AbstractThread
from camera.camera import Camera 
from queue import Queue
from microphone.microphone import _sentinelMic

_sentinel_camera_to_archiver = object()

class CameraThreadManager(AbstractThread):
    
    def __init__(self):
        self.pictures_amount = 20
        self.taps_count = 4
    '''
    expects already setup Mic
    taps_count amount of taps  before picture is taken
    pictures_amount amount of pictures before we will alert archiver  to get all the images 
    from the pictures folder and archive them
    '''
    def run(self, cam: Camera, queue: Queue, taps_count=None, pictures_amount=None):
        if taps_count is None: taps_count = self.taps_count
        if pictures_amount is None: pictures_amount = self.pictures_amount

        taps = 0
        pictures_taken = 0
        
        while self._running:
            queue_data = queue.get()
            if queue_data is _sentinelMic:
                taps += 1
                print(taps)
                if taps == taps_count:
                    cam.takeNPictures(1)
                    pictures_taken += 1    
                    taps = 0    
                if pictures_taken == pictures_amount:
                    queue.put(_sentinel_camera_to_archiver)
                    
                
