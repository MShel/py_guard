import math
import struct
from asyncio import coroutine

import pyaudio

'''
most of this class been taken from
http://stackoverflow.com/questions/4160175/detect-tap-with-pyaudio-from-live-mic
'''


class Mic:
    INITIAL_TAP_THRESHOLD = 0.010

    FORMAT = pyaudio.paInt16

    SHORT_NORMALIZE = (1.0 / 32768.0)

    CHANNELS = 2

    RATE = 44100

    INPUT_BLOCK_TIME = 0.05

    INPUT_FRAMES_PER_BLOCK = int(RATE * INPUT_BLOCK_TIME)

    OVERSENSITIVE = 15.0 / INPUT_BLOCK_TIME

    UNDERSENSITIVE = 120.0 / INPUT_BLOCK_TIME

    MAX_TAP_BLOCKS = 0.15 / INPUT_BLOCK_TIME

    MIC_DONE = 'mic_done'

    def __init__(self, config_object: dict):
        py_audio = pyaudio.PyAudio()
        self.stream = py_audio.open(format=self.FORMAT,
                                    channels=self.CHANNELS,
                                    rate=self.RATE,
                                    input=True,
                                    frames_per_buffer=self.INPUT_FRAMES_PER_BLOCK)
        self.tap_threshold = float(config_object['MICROPHONE']["tap_treshhold"])
        self.INPUT_BLOCK_TIME = float(config_object['MICROPHONE']["INPUT_BLOCK_TIME"])
        self.noisy_count = self.MAX_TAP_BLOCKS + 1
        self.quiet_count = 0
        self.error_count = 0
        self.mic_action = self._mic_action()
        # need send None to get to the first yield
        self.mic_action.send(None)

    @coroutine
    def _mic_action(self):
        while True:
            args = (yield)
            if args['action'] == 'listen':
                print(self.listen())
                if self.listen() is True:
                    yield self.MIC_DONE
            else:
                raise LookupError('Invalid microphone action')

    def get_rms(self, block):
        count = len(block) / 2
        formatConvertWave = "%dh" % (count)
        shorts = struct.unpack(formatConvertWave, block)

        # iterate over the block.
        sum_squares = 0.0
        for sample in shorts:
            # sample is a signed short in +/- 32768. 
            # normalize it to 1.0
            n = sample * self.SHORT_NORMALIZE
            sum_squares += n * n

        return math.sqrt(sum_squares / count)

    def listen(self):
        result = False
        try:
            block = self.stream.read(self.INPUT_FRAMES_PER_BLOCK)  # |
        except IOError as e:  # |---- just in case there is an error!
            self.error_count += 1  # |
            print("(%d) Error recording: %s" % (self.errorcount, e))  # |
            self.noisy_count = 1  # ]

        amplitude = self.get_rms(block)

        if amplitude > self.tap_threshold:  # if its to loud...
            self.quiet_count = 0
            self.noisy_count += 1
            if self.noisy_count > self.OVERSENSITIVE:
                self.tap_threshold *= 1.1  # turn down the sensitivity
        else:  # if its to quiet...
            if 1 <= self.noisy_count <= self.MAX_TAP_BLOCKS:
                result = True
            self.noisy_count = 0
            self.quiet_count += 1

            if self.quiet_count > self.UNDERSENSITIVE:
                self.tap_threshold *= 0.9  # turn up the sensitivity
        return result

    '''
    proxy to couroutine
    '''

    def send(self, action_dict: dict):
        return self.mic_action.send(action_dict)

    '''
    close running coroutine
    '''

    def close(self):
        self.mic_action.close()
