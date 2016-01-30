from cv2 import *
from datetime import datetime
_sentinelCamera = object()

# initialize the camera
class Camera:
    
    def __init__(self, queue):
        self.pictures_taken = 0
        self.camera = VideoCapture(0)
        self.queue = queue
    
    def takeNPictures(self, n: int, pictures_directory: str, pictures_amount: int):
        for i in (0, n):    
            s, img = self.camera.read()
            if s:  # frame captured without any errors
                waitKey(30)  # time for camera to focus
                imwrite(pictures_directory + str(datetime.today()) + ".jpg", img)  # save image
                self.pictures_taken += 1
                
                if self.pictures_taken == pictures_amount:
                    print('archiving')
                    self.queue.put(_sentinelCamera)
                    self.pictures_taken = 0
               
                