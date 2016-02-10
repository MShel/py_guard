from queue import Queue
import os
import smtplib
import mimetypes
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from sentinels import _sentinelSender

# initialize the camera
class Mailer:
    
    def __init__(self, queue: Queue, pictures_directory: str, emailTo: str, subject: str, emailFrom: str):
        self.queue = queue
        self.pictures_directory = pictures_directory
        self.emailTo = emailTo
        self.subject = subject
        self.emailFrom = emailFrom
        self.server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        self.server.ehlo()
        self.server.login('mshelemetev@gmail.com', '***************')
        
    def sendLastArchive(self, archiveName: str):
        result = False
        # Create the container (outer) email message.
        path =  os.path.join(archiveName)
        if os.path.isfile(path):
            outer = MIMEMultipart()
            outer['Subject'] = self.subject
            outer['From'] = self.emailFrom
            outer['To'] = self.emailTo
            outer.preamble = self.subject
            ctype, encoding = mimetypes.guess_type(path)
            maintype, subtype = ctype.split('/', 1)
            with open(path,'rb') as fp:
                msg = MIMEBase(maintype, subtype)
                msg.set_payload(fp.read())
                encoders.encode_base64(msg)
                msg.add_header('Content-Disposition', 'attachment', filename=archiveName)
            outer.attach(msg)
            result = self.server.sendmail(self.emailFrom, self.emailTo, outer.as_string())      
            self.server.close()
            self.queue.put(_sentinelSender)
        else:
            print(archiveName)
        return result
    
    def sendAll(self):
        for root, dirs, files in os.walk(self.pictures_directory):
            for file in files:
                if file.endswith('zip'):
                    os.remove(self.pictures_directory + file)


