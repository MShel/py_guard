from cv2 import *
from datetime import datetime
from threading import Timer
from asyncio import coroutine

# initialize the camera
class Camera:
    def __init__(self, config_object: dict):
        self.pictures_taken = 0
        self.camera = VideoCapture(0)
        self.pictures_directory = config_object["FILES"]["picture_directory"]
        self.pictures_amount = int(config_object["CAMERA"]["pictures_amount"])
        self.video_time_interval = int(config_object["CAMERA"]["video_interval"])
        self.camera_action = self._camera_action()
        self._camera_action.send(None)

    @coroutine
    def _camera_action(self):
        while True:
            args = (yield)
            if args['action'] == 'photos':
                self.take_some_pictures()
                yield 'done'
            elif args['action'] == 'video':
                self.record_some_video()
                yield 'done'
            else:
                print("Invalid action")

    def take_some_pictures(self):
        for i in range(0, self.pictures_amount + 1):
            s, img = self.camera.read()
            if s:  # frame captured without any errors
                waitKey(30)
                picturePath = self.pictures_directory + str(datetime.today()) + ".jpg"
                imwrite(picturePath, img)  # save image
                self.pictures_taken += 1
                print("pictures taken " + self.pictures_taken + "\n")
            if self.pictures_taken == self.pictures_amount:
                self.pictures_taken = 0
                self.camera.release()

    def record_some_video(self):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(self.pictures_directory + str(datetime.today()) + ".avi", fourcc, 20.0, (640, 480))
        video_timer = Timer(self.video_time_interval, lambda done: print("timer done"))
        video_timer.start()
        while self.camera.isOpened() and video_timer.finished.is_set() is True:
            ret, frame = self.camera.read()
            if ret == True:
                frame = cv2.flip(frame, 0)
                # write the flipped frame
                out.write(frame)
                self.camera.release()
                out.release()
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print('video recording failed')
                    break
            else:
                print('video recording failed')
                break

    '''
    proxy to couroutine
    '''
    def send(self,**kwargs):
       return self.camera_action.send(kwargs)

    '''
    close running coroutine
    '''
    def close(self)
        self.takeNPictures.close()