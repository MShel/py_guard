#!/usr/bin/env python
import getopt
import os
import re
import subprocess
import sys
from queue import Queue
from threading import Thread

from archiver.archiver_thread import ArchiverThreadManager
from archiver.snapshot_archiver import SnapshotArchiver
from camera.camera import Camera
from camera.camera_thread import CameraThreadManager
from microphone.microphone import Mic
from microphone.microphone_thread import MicrophoneThreadManager
from sender.mailer import Mailer
from sender.sender_thread import SenderThreadManager

sys.path.insert(0, os.getcwd())


# Get the args
def main(argv):
    # Clear the screen
    subprocess.call('clear', shell=True)
    try:
        opts, args = getopt.getopt(argv, 'h', ['email=', 'dblevel='])
        '''
         options:
          --email=test@test.com .. you should have mail server setup
          or later I'll implement some ssl encrypted communication with my server which will
          push stuff there process and send to an email specified
          ...

          Another option

          --dblevel=20 noise level
         '''

        for opt, arg in opts:

            if opt in ('--help', '-h'):
                print('HEEELLP')
                sys.exit(0)

            if opt == '--email' and re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", arg):
                email = arg

            if opt == '--dblevel':
                db_level = arg

        '''
        need to spin the threads and get all the jazz up and running
        probably need a separate config parser and starter classes...?
        '''
        queue_for_everything = Queue()
        mic = Mic(queue_for_everything)

        archiver = SnapshotArchiver(queue_for_everything)
        archiver_thread_manager = ArchiverThreadManager()
        archiver_thread = Thread(target=archiver_thread_manager.run,
                                 args=(archiver, queue_for_everything, './pictures/'))
        archiver_thread.start()

        mic_thread_manager = MicrophoneThreadManager()
        microphone_thread = Thread(target=mic_thread_manager.run, args=(mic,))
        microphone_thread.start()

        camera = Camera(queue_for_everything)
        camera_thread_manager = CameraThreadManager()
        camera_thread = Thread(target=camera_thread_manager.run, args=(camera, queue_for_everything))
        camera_thread.start()

        mailer = Mailer(queue_for_everything, './pictures/', 'mshelemetev@gmail.com', 'pyGuard name',
                        'pyGuard@localhost.com')
        sender_thread_manager = SenderThreadManager()
        sender_thread = Thread(target=sender_thread_manager.run, args=(mailer, queue_for_everything))
        sender_thread.start()

        '''
        queue: Queue, pictures_directory: str, emailTo: str, subject: str, emailFrom: str
        time.sleep(15)
        mic_thread_manager.stop()
        camera_thread_manager.stop()
        camera_thread.join()
        microphone_thread.join()
        '''

    except (getopt.GetoptError, IndexError, ImportError) as e:
        print(e)
        sys.exit(2)
    except Exception as e:
        print(e)
        sys.exit(2)
    except KeyboardInterrupt:
        print('????test')
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
