#!/usr/bin/env python
import sys, getopt, subprocess
import os
from queue import Queue
import re
from threading import Thread
from microphone.microphone import Mic
from pprint import pprint
from microphone.microphone_thread import MicrophoneThread
import time

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
          or later I'll implement some ssl encrypted communication with my server which will push stuff there process and send to an email specified
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
        need to spin the threads and get all the juzz up and running
        '''
        q_microphone = Queue()     
        mic = Mic(q_microphone)
        mic_thread_manager = MicrophoneThread()   
        microphone_thread = Thread(target=mic_thread_manager.run, args=(mic,))
        microphone_thread.start()
        
        
    except getopt.GetoptError:
        print('test1')
        sys.exit(2)
    except PermissionError:
        print('test1')
        sys.exit(2)
    except Exception as e:
        print(e)
        sys.exit(2)
    except IndexError:
        print('test1')
        sys.exit(2)
    except KeyboardInterrupt:
        mic_thread_manager.stop()
        microphone_thread.join()
        print('????test')
        sys.exit(1)
    ''''
    except ImportError:
        sys.exit(2)    
    '''

        
    
if __name__ == "__main__":
    main(sys.argv[1:])
