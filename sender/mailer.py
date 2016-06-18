import email.mime.multipart
import mimetypes
import os
import smtplib
from asyncio import coroutine
from email import encoders
from email.mime.base import MIMEBase


# initialize email
class Mailer:
    # value to return
    MAILER_DONE = 'mailer_done'

    def __init__(self, config_object: dict):
        self.pictures_directory = config_object["FILES"]["pictures_directory"]
        self.emailTo = config_object["EMAILS"]["email"]
        self.subject = config_object["EMAILS"]["title"]
        self.emailFrom = config_object["EMAILS"]["pyGuard@localhost"]
        self.server = smtplib.SMTP_SSL(config_object["EMAILS"]["server_address"], config_object["EMAILS"]["port"])
        self.server.ehlo()
        self.server.login(config_object["EMAILS"]["email"], config_object["EMAILS"]["password"])
        self.mailer_action = self._mailer_action()
        # need send None to get to the first yield
        self.mailer_action.send(None)

    @coroutine
    def _mailer_action(self):
        while True:
            args = (yield)
            if args['action'] == 'last':
                if args['last_archive_name']:
                    self.send_last_archive(args['last_archive_name'])
                yield self.MAILER_DONE
            elif args['action'] == 'all':
                self.send_all()
                yield self.MAILER_DONE
            else:
                raise LookupError('Invalid mailer action')

    def send_last_archive(self, archive_name: object) -> object:
        # Create the container (outer) email message.
        path = os.path.join(archive_name)
        if os.path.isfile(path):
            outer = email.mime.multipart.MIMEMultipart()
            outer['Subject'] = self.subject
            outer['From'] = self.emailFrom
            outer['To'] = self.emailTo
            outer.preamble = self.subject
            ctype, encoding = mimetypes.guess_type(path)
            maintype, subtype = ctype.split('/', 1)
            with open(path, 'rb') as fp:
                msg = MIMEBase(maintype, subtype)
                msg.set_payload(fp.read())
                encoders.encode_base64(msg)
                msg.add_header('Content-Disposition', 'attachment', filename=archive_name)
            outer.attach(msg)
            self.server.sendmail(self.emailFrom, self.emailTo, outer.as_string())
            self.server.close()

    def send_all(self):
        for root, dirs, files in os.walk(self.pictures_directory):
            for file in files:
                if file.endswith('zip'):
                    file_path = self.pictures_directory + file
                    self.send_last_archive(file_path)
                    os.remove(self.pictures_directory + file)

    '''
    proxy to couroutine
    '''

    def send(self, action_dict: dict):
        return self.mailer_action.send(action_dict)

    '''
    close running coroutine
    '''

    def close(self):
        self.mailer_action.close()
