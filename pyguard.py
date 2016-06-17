#!/usr/bin/env python
import getopt
import os
import subprocess
import sys
from queue import Queue
from threading import Thread

from archiver.archiver_thread import ArchiverThreadManager
from archiver.snapshot_archiver import SnapshotArchiver
from camera.camera import Camera
from camera.camera_thread import CameraThreadManager
from config.config import Config
from microphone.microphone import Mic
from microphone.microphone_thread import MicrophoneThreadManager
from sender.mailer import Mailer
from sender.sender_thread import SenderThreadManager

sys.path.insert(0, os.getcwd())


# Get the args
def main():
    # Clear the screen
    subprocess.call('clear', shell=True)
    config_object = Config(os.getcwd() + '/config/config.ini').raw_config_object

    try:

        '''
        need to spin the threads and get all the jazz up and running
        probably need a separate config parser and starter classes...?
        '''
        mic = Mic(config_object)
        #tell mic to listen...
        mic.send({'action':'listen'})
        camera = Camera(config_object)
        #tell camera to take some pictures...
        camera_res = camera.send({'action':'photos'})

        queue_for_everything = Queue()
        archiver = SnapshotArchiver(queue_for_everything, config_object)
        archiver_thread_manager = ArchiverThreadManager()
        archiver_thread = Thread(target=archiver_thread_manager.run,
                                 args=(archiver, queue_for_everything))
        archiver_thread.start()

        mic_thread_manager = MicrophoneThreadManager()
        microphone_thread = Thread(target=mic_thread_manager.run, args=(mic,))
        microphone_thread.start()



        if camera_res == camera.CAMERA_DONE:
            mailer = Mailer(queue_for_everything, config_object)
            sender_thread_manager = SenderThreadManager()
            sender_thread = Thread(target=sender_thread_manager.run, args=(mailer, queue_for_everything))
            sender_thread.start()

    except LookupError as e:
        print(e)
        sys.exit(2)

    except KeyboardInterrupt:
        print('keyboard interruption')
        camera.close()
        mic.close()
        sys.exit(1)


if __name__ == "__main__":
    main()
