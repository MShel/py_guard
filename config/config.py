import ConfigParser

def get_config_object(filename :str):
    parsed_config = ConfigParser.ConfigParser().read(filename)
    return parsed_config