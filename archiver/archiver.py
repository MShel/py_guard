import os
import zipfile
from asyncio import coroutine
from datetime import datetime


class Archiver:
    ARCHIVER_DONE = 'arch_done'

    def __init__(self, config_object: dict, filetype='jpg'):
        self.zfilename = None
        self.file_direcory = config_object["FILES"]["picture_directory"]
        self.archive_type = 'zip'
        self.file_type = filetype
        self.archiver_action = self._archiver_action()
        # need send None to get to the first yield
        self.archiver_action.send(None)

    @coroutine
    def _archiver_action(self):
        while True:
            args = (yield)
            if args['action'] == 'archive':
                self.archive_files()
                yield self.ARCHIVER_DONE
            elif args['action'] == 'clearup':
                self.clean_files()
                yield self.ARCHIVER_DONE
            else:
                raise LookupError('Invalid archiver action')

    def archive_files(self) -> str:
        self.zfilename = self.file_direcory + str(datetime.today()) + 'snapshots.' + self.archive_type
        ziped_file = zipfile.ZipFile(self.zfilename, 'w')
        for root, dirs, files in os.walk(self.file_direcory):
            for file in files:
                if file.endswith(self.file_type) is True:
                    ziped_file.write(os.path.join(root, file))

    def clean_files(self):
        for root, dirs, files in os.walk(self.file_direcory):
            for file in files:
                if file.endswith(self.file_type) or file.endswith('snapshots.' + self.archive_type) is True:
                    os.remove(self.file_direcory + file)

    '''
    proxy to couroutine
    '''

    def send(self, action_dict: dict):
        return self.archiver_action.send(action_dict)

    '''
    close running coroutine
    '''

    def close(self):
        self.archiver_action.close()
