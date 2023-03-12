import requests
from ddddocr import DdddOcr
import re
from Encrypt import Encrypt
from Course import QNDXX_NEW_COURSE

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
        self.email = ''
        self.encrypt=Encrypt()

    def get_cookie(self):
        for i in range(self.get_cookies_turn):
            # cookies = self.get_login_cookie_with_selenium()
            print(f'[INFO] Try to get cookie ... {i}/{self.get_cookies_turn}')
            cookies = self.get_cookie_with_requests()
            if cookies:
                self.cookies = 'PHPSESSID=' + cookies
                self.headers["Cookie"] = self.cookies
                print('[INFO] Get cookie successfully.')
                return True
        print('[ERROR] Get cookie error! please check your password.')
        return False


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

            # save captcha
            # with open('cap.jpg', 'wb') as f:
            #     f.write(cap.content)

            print(f'[INFO] Captcha OCR: {cap_text}')
            # print(S.cookies.get_dict())
            _csrf_mobile = S.cookies.get_dict()['_csrf_mobile']
            headers['Origin'] = "https://m.bjyouth.net"
            login_username = self.encrypt.encrypt(self.username)
            login_password = self.encrypt.encrypt(self.password)
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
            return ''

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
        self.email = config['email'] or ''

    def study(self):
        try:
            # study_url = self.course.study_url % self.org_id
            # r = requests.get(url=study_url, headers=self.headers, timeout=5)
            data= {"id":self.course.id,"org_id":self.org_id}
            r = requests.post(url="https://m.bjyouth.net/dxx/check",headers=self.headers, timeout=5,json=data)
            r.status_code
            if r.text:
                print(
                    f'[ERROR] The url{self.study_url} maybe not correct or the website changed'
                )
                return True
            print(f'[INFO] Study complete')
            raw_message = f"{self.username} learned id={self.course.id} :\n{self.course.title[6:10] + '...'}\nend.jpg:\n{self.course.end_img_url}\nstudy url:\n{self.course.study_url % '172442'}"
            self.send_message(raw_message)
            return 1
        except:
            print('[ERROR] Study fail')
            return False
