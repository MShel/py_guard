from microphone.microphone import Mic

class MicrophoneThread():

    def __init__(self):
        self._running = True
    
    def stop(self):
        self._running = False
    
    '''
    expects already setup Mic
    '''
    def run(self, mic: Mic):
        while self._running:
            mic.listen()        