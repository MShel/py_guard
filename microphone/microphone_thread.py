from microphone.microphone import Mic
from threads.abstract_thread import AbstractThread

class MicrophoneThreadManager(AbstractThread):
    
    '''
    expects already setup Mic
    '''
    def run(self, mic: Mic):
        while self._running:
            mic.listen()