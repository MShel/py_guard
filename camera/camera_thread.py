from threads.abstract_thread import AbstractThread
from camera.camera import Camera 
from queue import Queue
from microphone.microphone import _sentinelMic

class CameraThreadManager(AbstractThread):
    
    '''
    expects already setup Mic
    '''
    def run(self, cam: Camera,queue: Queue):
        while self._running:
            queue_data = queue.get()
            if queue_data is _sentinelMic:
                cam.takeNPictures(3)
