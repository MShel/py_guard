import ConfigParser

class Config:
    
    def __init__(self, filename:str) -> dict:
        res = []
        raw_config_object = self.get_config_object(filename)
        res = self.validate(raw_config_object)
        return res
    
    def get_config_object(file :fp) -> dict:
        parsed_config = ConfigParser.ConfigParser().readfp(filename)
        return parsed_config
   
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
