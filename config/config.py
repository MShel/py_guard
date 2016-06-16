import json
import os
import re
from configparser import ConfigParser
from pprint import pprint

class Config:
    raw_config_object = None

    EMAILS_SECTION = ''

    MICROPHONE_SECTION = ''

    CAMERA_SECTION = ''

    FILES_SECTION = ''

    def __init__(self, filename: str) -> dict:
        self.raw_config_object = self.get_config_object(filename)
        self.EMAILS_SECTION = 'EMAILS'
        self.MICROPHONE_SECTION = 'MICROPHONE'
        self.CAMERA_SECTION = 'CAMERA'
        self.FILES_SECTION = 'FILES'
        self.validate()

    '''
    need to raise different
    exceptions:
        warnings: (if emails is not specified)
        error: (if picture directory is not writable,
        or microphone details are not ints )
    '''

    def validate(self):
        # TODO add all kind of crappy rules
        if re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                    self.raw_config_object[self.EMAILS_SECTION]['email']) == None:
            raise ValueError('Email is not valid')

        if not os.access(self.raw_config_object[self.FILES_SECTION]['picture_directory'], os.W_OK):
            raise ValueError('Picture directory is not writable')

    @staticmethod
    def get_config_object(filename) -> dict:
        config_parser = ConfigParser()
        config_parser.read(filename)
        return config_parser

    def serialize(self):
        return json.JSONEncoder.default(self.raw_config_object)
