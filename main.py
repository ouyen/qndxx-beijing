import argparse
import json
import os
import re
import smtplib
from base64 import b64encode
from email.header import Header
from email.mime.text import MIMEText

import requests
import yaml
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
from ddddocr import DdddOcr


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
            return 1
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
            return 1
        except:
            print('[ERROR] Failed to read mail config')
            return 0


class QNDXX_NEW_COURSE():
    def __init__(self) -> None:
        self.id = 59
        self.title = '青年大学习：江山就是人民，人民就是江山'
        self.url = "https://h5.cyol.com/special/daxuexi/byw1m1kn1s/m.html?t=1&z=201",
        # self.org_id = 172442  #"北京市海淀团区委"
        self.end_img_url = 'https://h5.cyol.com/special/daxuexi/byw1m1kn1s/images/end.jpg'  #example
        self.study_url = f"https://m.bjyouth.net/dxx/check?id={self.id}&org_id=%s"
        self.need_update = True

    def update(self, headers):
        try:
            r = requests.get("https://m.bjyouth.net/dxx/index",
                             headers=headers,
                             timeout=5)
            r.status_code
            index = json.loads(r.text)
            self.id = index['newCourse']['id']
            self.title = index['newCourse']['title']
            self.url = index['newCourse']['url']
            # self.org_id = index['rank'][0]['data'][1]['org_id']
            i = self.url.find("/m.html")
            self.end_img_url = self.url[:i] + '/images/end.jpg'
            self.study_url = f"https://m.bjyouth.net/dxx/check?id={self.id}&org_id=%s"
            print('[INFO] Class updated success')
            return 1
        except:
            print('[ERROR] Class update failed')
            return 0


class Youth():
    def __init__(self) -> None:
        self.cookies = ''
        self.username = ''
        self.password = ''
        self.get_cookies_turn = 5
        self.course = QNDXX_NEW_COURSE()
        self.ua = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6303004c)"
        self.headers = {
            "Host": "m.bjyouth.net",
            "User-Agent": self.ua,
            "Cookie": '',
            "Referer": "https://m.bjyouth.net/qndxx/index.html"
        }
        self.send_message_url = ''
        self.org_id = '172442'  #"北京市海淀团区委"
        self.send_message_org_id = '172442'
        self.mailer = Mailer()
        self.email = ''

    def get_cookie(self):
        for i in range(self.get_cookies_turn):
            # cookies = self.get_login_cookie_with_selenium()
            print(f'[INFO] Try to get cookie ... {i}/{self.get_cookies_turn}')
            cookies = self.get_cookie_with_requests()
            if cookies:
                self.cookies = 'PHPSESSID=' + cookies
                self.headers["Cookie"] = self.cookies
                print('[INFO] Get cookie successfully.')
                return 1
        print('[ERROR] Get cookie error! please check your password.')
        return 0

    def encrypt(self, password, public_key=''):
        if public_key == '':
            public_key = "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQD5uIDebA2qU746e/NVPiQSBA0Q3J8/G23zfrwMz4qoip1vuKaVZykuMtsAkCJFZhEcmuaOVl8nAor7cz/KZe8ZCNInbXp2kUQNjJiOPwEhkGiVvxvU5V5vCK4mzGZhhawF5cI/pw2GJDSKbXK05YHXVtOAmg17zB1iJf+ie28TbwIDAQAB\n-----END PUBLIC KEY-----"
        rsa_key = RSA.importKey(public_key)
        cipher = Cipher_pksc1_v1_5.new(rsa_key)
        cipher_text = b64encode(cipher.encrypt(password.encode()))
        return cipher_text.decode()

    def get_cookie_with_requests(self):
        try:
            S = requests.Session()
            headers = {"Host": "m.bjyouth.net", "User-Agent": self.ua}
            r = S.get(url="https://m.bjyouth.net/site/login",
                      headers=headers,
                      timeout=5)
            r.status_code
            cap_url = "https://m.bjyouth.net" + re.findall(
                r'src="/site/captcha.+" alt=', r.text)[0][5:-6]
            headers["Referer"] = "https://m.bjyouth.net/site/login"
            cap = S.get(url=cap_url, headers=headers, timeout=5)
            cap.status_code
            ocr = DdddOcr()
            cap_text = ocr.classification(cap.content)
            print(f'[INFO] Captcha OCR: {cap_text}')
            _csrf_mobile = S.cookies.get_dict()['_csrf_mobile']
            headers['Origin'] = "https://m.bjyouth.net"
            login_username = self.encrypt(self.username)
            login_password = self.encrypt(self.password)
            login_r = S.post('https://m.bjyouth.net/site/login',
                             headers=headers,
                             data={
                                 '_csrf_mobile': _csrf_mobile,
                                 'Login[username]': login_username,
                                 'Login[password]': login_password,
                                 'Login[verifyCode]': cap_text
                             },
                             timeout=5)
            return login_r.cookies.get_dict()['PHPSESSID']
        except:
            return 0

    def send_message(self, raw_message: str):
        if self.send_message_url != '':
            message = requests.utils.quote(raw_message)
            try:
                print('[INFO] Sending message')
                url = self.send_message_url % message
                r = requests.get(url, timeout=5)
                r.status_code
                return 1
            except:
                print('[ERROR] Send message failed')
                return 0

    def read_config(self, config):
        self.username = config['username']
        self.password = config['password']
        if not (self.username and self.password):
            raise "username and password cannot be blank!!!"
        self.org_id = config['org_id'] or self.org_id
        self.send_message_url = config['message_url']
        self.send_message_org_id = config['send_message_org_id'] or self.org_id
        self.email = config['email'] or ''

    def study(self):
        try:
            study_url = self.course.study_url % self.org_id
            r = requests.get(url=study_url, headers=self.headers, timeout=5)
            r.status_code
            if r.text:
                print(
                    f'[ERROR] The url{study_url} maybe not correct or the website changed'
                )
                return 0
            print(f'[INFO] Study complete')
            raw_message = f"{self.username} learned id={self.course.id} :\n{self.course.title[6:10] + '...'}\nend.jpg:\n{self.course.end_img_url}\nstudy url:\n{self.course.study_url % self.send_message_org_id}"
            if self.email and self.mailer:
                self.mailer.send_mail(self.email, raw_message)
            self.send_message(raw_message)
            return 1
        except:
            print('[ERROR] Study fail')
            return 0


def main(remote_config=''):
    youth = Youth()
    course = youth.course
    print('[INFO] Read config from config.yaml')
    if remote_config:
        print('[INFO] Read remote config')
        try:
            r = requests.get(remote_config, timeout=5)
            r.status_code
            print('[INFO] Get remote config succeed')
            try:
                config_dict = yaml.safe_load(r.text)
            except:
                print('[ERROR] Please check your remote config')
                return 0
        except:
            print('[ERROR] Get remote config failed')
            return 0
    else:
        with open('config.yaml', 'r') as f:
            config_dict = yaml.safe_load(f)
    mailer = youth.mailer
    mailer.read_config(config_dict['Mailer'])
    for single_config in config_dict['youth']:
        print(single_config['username'], 'Start')
        youth.read_config(single_config)
        if not youth.get_cookie():
            continue
        if (course.need_update):
            if not course.update(youth.headers):
                continue
            course.need_update = False
        if not youth.study():
            continue
    return 1


def main_cli(args):
    print('[INFO] Read config from command line parameters')
    print('[INFO] Start')
    youth = Youth()
    # youth.username = args.username
    # youth.password = args.password
    # youth.org_id = args.org_id
    youth.username = args["USERNAME"]
    youth.password = args["PASSWORD"]
    youth.org_id = args["ORG_ID"]
    if not youth.get_cookie():
        return 0
    if not youth.course.update(youth.headers):
        return 0
    if not youth.study():
        return 0


if __name__ == '__main__':
    # parser = argparse.ArgumentParser()
    # parser.add_argument('--username', type=str)
    # parser.add_argument('--password', type=str)
    # parser.add_argument('--org_id', type=str)
    # parser.add_argument('--remote_config', type=str)
    # args = parser.parse_args()
    ENV={_i:os.getenv(_i) for _i in ['PASSWORD','USERNAME','ORG_ID','REMOTE_CONFIG']}
    if (ENV['REMOTE_CONFIG']):
        main(ENV['REMOTE_CONFIG'])
    # elif (args.username and args.password and args.org_id):
    elif(ENV['USERNAME'] and ENV['PASSWORD'] and ENV['ORG_ID']):
        main_cli(ENV)
    else:
        main()
