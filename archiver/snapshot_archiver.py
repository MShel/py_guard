from queue import Queue
from datetime import datetime
import os
import zipfile
# initialize the camera
class SnapshotArchiver:
    
    def __init__(self):
        self.zfilename = None
        self.pictures_directory = None
    
    def archivePictures(self,pictures_directory: str) -> str:
        self.zfilename = pictures_directory+str(datetime.today())+'snapshots.zip'
        self.pictures_directory = pictures_directory
        
        ziped_file = zipfile.ZipFile(self.zfilename, 'w')
        for root, dirs, files in os.walk(pictures_directory):
            for file in files:
                ziped_file.write(os.path.join(root, file))
        
        return self.zfilename
    
    def cleanPictures(self):
        for root, dirs, files in os.walk(self.pictures_directory):
            for file in files:
                if not self.zfilename.endsWith('zip'):
                    os.remove(self.pictures_directory+file.name)
        