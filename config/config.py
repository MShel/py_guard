from configparser import ConfigParser
from pprint import pprint

class Config:
    raw_config_object = None

    def __init__(self, filename: str) -> dict:
        self.raw_config_object = get_config_object(filename)

    '''
    need to raise different 
    exceptions:
        warnings: (if emails is not specified)
        error: (if picture directory is not writable, 
        or microphone details are not ints )  
    '''

    def validate(self, raw_config_object):
        validated_object = []
        return validated_object


def get_config_object(filename) -> dict:
    config_parser = ConfigParser()
    config_parser.read(filename)

    return config_parser


if __name__ == "__main__":
    conf_obj = get_config_object('config.ini')
    pprint(conf_obj.sections())
    pprint(conf_obj['DEFAULT']['email'])