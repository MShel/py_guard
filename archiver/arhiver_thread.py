from threads.abstract_thread import AbstractThread
from camera.camera import Camera 
from queue import Queue
from microphone.microphone import _sentinelMic
from datetime import datetime
import time

class CameraThreadManager(AbstractThread):
    
    '''
    expects already setup Mic
    '''
    def run(self, cam: Camera,queue: Queue):
        taps = 0
        while self._running:
            queue_data = queue.get()
            if queue_data is _sentinelMic:
                taps +=1
                print(taps)
                if taps == 4:
                    cam.takeNPictures(1)
                    taps = 0    