from queue import Queue
import os
import smtplib
import mimetypes
from email import encoders
from email.mime.multipart import *
from sentinels import _sentinelSender

# initialize the camera
class Mailer:
    
    def __init__(self, queue: Queue, pictures_directory: str, emailTo: str, subject: str, emailFrom: str):
        self.queue = queue
        self.pictures_directory = pictures_directory
        self.emailTo = emailTo
        self.subject = subject
        self.emailFrom = emailFrom
        
    def sendLastArchive(self, archiveName: str):
        result = False
        # Create the container (outer) email message.
        if os.path.isfile(self.pictures_directory, archiveName):
            outer = MIMEMultipart()
            outer['Subject'] = self.subject
            outer['From'] = self.emailFrom
            outer['To'] = self.emailTo
            outer.preamble = self.subject
            path =  os.path.join(self.pictures_directory, archiveName)
            ctype, encoding = mimetypes.guess_type(path)
            maintype, subtype = ctype.split('/', 1)
            with open(path,'rb') as fp:
                msg = MIMEBase(maintype, subtype)
                msg.set_payload(fp.read())
                encoders.encode_base64(msg)
                msg.add_header('Content-Disposition', 'attachment', filename=archiveName)
            outer.attach(msg)
           
            with smtplib.SMTP('localhost') as s:
                result = s.sendmail(self.emailFrom, self.EmailTo, outer.as_string())      
            
            self.queue.put(_sentinelSender)
        return result
    
    def sendAll(self):
        for root, dirs, files in os.walk(self.pictures_directory):
            for file in files:
                if file.endswith('zip'):
                    os.remove(self.pictures_directory + file)
