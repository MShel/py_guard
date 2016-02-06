from queue import Queue
from datetime import datetime
import os
from sentinels import _sentinelSender
import smtplib
import zipfile
from email import encoders

from email.mime.multipart import *

# initialize the camera
class Mailer:
    
    def __init__(self, queue: Queue, pictures_directory: str, emailTo: str, subject: str, emailFrom ='py_guard@localhost.com'):
        self.queue = queue
        self.pictures_directory = pictures_directory
        self.emailTo = emailTo
        self.subject = subject
        self.emailFrom = emailFrom
        
    def sendLastArchive(self, archiveName: str):
        '''
        send archive
        '''
        # Create the container (outer) email message.
        msg = MIMEMultipart()
        msg['Subject'] = 'Our family reunion'
        msg['From'] = self.emailFrom
        msg['To'] = self.emailTo
        msg.preamble = 'Our family reunion'
        msg = MIMEBase('application', 'zip')
        msg.set_payload(zipfile.ZipFile(archiveName, 'w').read())
        encoders.encode_base64(msg)
        msg.add_header('Content-Disposition', 'attachment', 
               filename=archiveName + '.zip')
        msg.attach(msg)
        self.queue.put(_sentinelSender)
      
    def sendAll(self):
        for root, dirs, files in os.walk(self.pictures_directory):
            for file in files:
                if file.endswith('zip'):
                    os.remove(self.pictures_directory + file)
