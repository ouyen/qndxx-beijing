from email.header import Header
from email.mime.text import MIMEText
import smtplib

class Mailer():
    def __init__(self) -> None:
        self.connect = ''
        self.connect_port = 25
        self.login_address = ""
        self.login_password = ""
        self.send_address = ""

    def send_mail(self, receiver_address, text):
        message = MIMEText(text, 'plain', 'utf-8')
        message['From'] = Header("qndxx")
        message['Subject'] = Header('QNDXX success!')
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(self.connect, self.connect_port)
            smtpObj.login(self.login_address, self.login_password)
            smtpObj.sendmail(self.send_address, receiver_address,
                             message.as_string())
            print('[INFO] Mail sent successfully')
            return True
        except:
            print('[ERROR] Failed to send mail')

    def read_config(self, config_dict: dict):
        try:
            self.connect = config_dict['connect']
            self.connect_port = config_dict['port'] or 25
            self.login_address = config_dict['login_address']
            self.login_password = config_dict['login_password']
            self.send_address = config_dict[
                'send_address'] or self.login_address
            return True
        except:
            print('[ERROR] Failed to read mail config')
            return False