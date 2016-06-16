from cv2 import *
from datetime import datetime

from sentinels import Sentinel


# initialize the camera
class Camera:
    def __init__(self, queue, config_object: dict):
        self.pictures_taken = 0
        self.camera = VideoCapture(0)
        self.pictures_directory = config_object["FILES"]["picture_directory"]
        self.pictures_amount = int(float(config_object["CAMERA"]["pictures_amount"]))
        self.queue = queue

    def takeNPictures(self):
        for i in range(0, self.pictures_amount + 1):
            s, img = self.camera.read()
            if s:  # frame captured without any errors
                waitKey(30)
                picturePath = self.pictures_directory + str(datetime.today()) + ".jpg"
                imwrite(picturePath, img)  # save image
                self.pictures_taken += 1
                #print("pictures taken "+self.pictures_taken+"\n")
                if self.pictures_taken == self.pictures_amount:
                    print("Put archiving Sentinel \n")
                    sentinel = Sentinel(datetime.now(), Sentinel.archiveAction, picturePath)
                    self.queue.put(sentinel)
                    self.pictures_taken = 0
