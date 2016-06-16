import os
import zipfile
from datetime import datetime
from queue import Queue

from sentinels import Sentinel


# initialize the camera
class SnapshotArchiver:
    def __init__(self, queue: Queue, config_object: dict):
        self.zfilename = None
        self.pictures_directory = config_object["FILES"]["picture_directory"]
        self.queue = queue

    def archivePictures(self) -> str:
        self.zfilename = self.pictures_directory + str(datetime.today()) + 'snapshots.zip'
        self.pictures_directory = self.pictures_directory

        ziped_file = zipfile.ZipFile(self.zfilename, 'w')
        for root, dirs, files in os.walk(self.pictures_directory):
            for file in files:
                if file.endswith('jpg') is True:
                    ziped_file.write(os.path.join(root, file))
        self.cleanPictures()
        sentinel = Sentinel(datetime.now(), Sentinel.senderAction, self.zfilename)
        self.queue.put(sentinel)

    def cleanPictures(self):
        for root, dirs, files in os.walk(self.pictures_directory):
            for file in files:
                if file.endswith('jpg') is True:
                    os.remove(self.pictures_directory + file)
