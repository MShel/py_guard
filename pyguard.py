#!/usr/bin/env python
import os
import subprocess
import sys

from archiver.archiver import Archiver
from camera.camera import Camera
from config.config import Config
from microphone.microphone import Mic
from sender.mailer import Mailer

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
        camera = Camera(config_object)
        archiver = Archiver(config_object)
        mailer = Mailer(config_object)

        while True:
            mic_response = mic.send({'action': 'listen'})
            print(".", end="", flush=True)

            if mic_response == mic.MIC_DONE:
                camera_res = camera.send({'action': 'photos'})
                print('taking photos')
                if camera_res == camera.CAMERA_DONE:
                    archiver_res = archiver.send({'action': 'archive'})
                    print('archiving...')
                    if archiver_res == archiver.ARCHIVER_DONE and archiver.zfilename is not None:
                        print('sending mail')
                        mailer_done = mailer.send({'action': 'last', 'last_archive_name': archiver.zfilename})
                        if mailer_done == mailer.MAILER_DONE:
                            print('...cleaning up')
                            archiver.send({'action': 'clearup'})
                            print('cycle done...')

    except LookupError as e:
        print(e)
        sys.exit(2)

    except KeyboardInterrupt:
        print('keyboard interruption')
        camera.close()
        mic.close()
        archiver.close()
        mailer.close()
        sys.exit(1)


if __name__ == "__main__":
    main()
