from cv2 import *
from queue import Queue
from datetime import datetime
import time
# initialize the camera
class Camera:
    
    def __init__(self, queue: Queue):
        self.camera = VideoCapture(0)
        self.queue = queue
        self.sentinelCam = object()
    
    
    def takeNPictures(self, n: int):
        for i in (0, n):    
            s, img = self.camera.read()
            if s:  # frame captured without any errors
                waitKey(15)  # time for camera to focus
                imwrite("./pictures/" + str(datetime.today()) + ".jpg", img)  # save image
                #self.queue.put(self.sentinelCam)