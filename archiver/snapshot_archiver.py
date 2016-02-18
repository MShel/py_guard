from queue import Queue
from datetime import datetime
import os
import zipfile
from sentinels import Sentinel

# initialize the camera
class SnapshotArchiver:
    
    def __init__(self, queue: Queue):
        self.zfilename = None
        self.pictures_directory = None
        self.queue = queue
    
    def archivePictures(self, pictures_directory: str) -> str:
        self.zfilename = pictures_directory + str(datetime.today()) + 'snapshots.zip'
        self.pictures_directory = pictures_directory
        
        ziped_file = zipfile.ZipFile(self.zfilename, 'w')
        for root, dirs, files in os.walk(pictures_directory):
            for file in files:
                if not file.endswith('zip'):
                    ziped_file.write(os.path.join(root, file))
        self.cleanPictures()
        sentinel = Sentinel(datetime.now(), Sentinel.senderAction, self.zfilename)
        self.queue.put(sentinel)
    
    def cleanPictures(self):
        for root, dirs, files in os.walk(self.pictures_directory):
            for file in files:
                if not file.endswith('zip'):
                    os.remove(self.pictures_directory + file)
