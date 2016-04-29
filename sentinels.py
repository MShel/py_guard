import datetime
from json import dumps

class Sentinel:
    archiveAction = 'archive'
    microphoneAction = 'mic'
    senderAction = 'send'
    
    _dateCreated = None
    _action = ''
    _meta = ''
    
    '''
    _dateCreated will be used later to keep track of stats
    _meta something we might need to transfer to other resources
    _action is property that we check for 
    '''
    def __init__(self, dateCreated : datetime.datetime, action :str, meta :str):
        self._dateCreated = dateCreated
        self._action = action
        self._meta = meta
    
    def get_name(self):
        return self._sentinelName
    
    def get_action(self) -> object:
        return self._action
    
    def get_dateCreated(self):
        return self._dateCreated
    
    def get_meta(self):
        return self._meta
        
    def __str__(self):
        self._dateCreated = self._dateCreated.isoformat()
        return dumps(self, default=lambda o: o.__dict__,
            sort_keys=True, indent=4)