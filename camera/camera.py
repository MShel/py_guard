from asyncio import coroutine
from datetime import datetime
from threading import Timer

from cv2 import *


# initialize the camera
class Camera:
    # value to return
    CAMERA_DONE = 'cam_done'

    def __init__(self, config_object: dict):
        self.pictures_taken = 0
        self.camera = VideoCapture(0)
        self.pictures_directory = config_object["FILES"]["picture_directory"]
        self.pictures_amount = int(config_object["CAMERA"]["pictures_amount"])
        self.video_time_interval = int(config_object["CAMERA"]["video_interval"])
        self.camera_action = self._camera_action()
        # need send None to get to the first yield
        self.camera_action.send(None)

    @coroutine
    def _camera_action(self):
        while True:
            args = (yield)
            print(args['action'])
            if args['action'] == 'photos':
                self.take_some_pictures()
                yield self.CAMERA_DONE
            elif args['action'] == 'video':
                self.record_some_video()
                yield self.CAMERA_DONE
            else:
                raise LookupError('Invalid camera action')

    def take_some_pictures(self):
        for i in range(0, self.pictures_amount + 1):
            s, img = self.camera.read()
            if s:  # frame captured without any errors
                waitKey(30)
                picturePath = self.pictures_directory + str(datetime.today()) + ".jpg"
                imwrite(picturePath, img)  # save image
                self.pictures_taken += 1
                print("pictures taken " + str(self.pictures_taken) + "\n")
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
            if ret is True:
                frame = cv2.flip(frame, 0)
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

    def send(self, action_dict: dict):
        return self.camera_action.send(action_dict)

    '''
    close running coroutine
    '''

    def close(self):
        self.camera_action.close()
