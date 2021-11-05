# from selenium import webdriver
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.common.by import By
import json
# import time
# from datetime import date
import requests
from ddddocr import DdddOcr
from re import findall
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pksc1_v1_5
from Crypto.PublicKey import RSA
# import base64
from base64 import b64encode


class QNDXX_NEW_COURSE():
    def __init__(self) -> None:
        self.id = 59
        self.title = '青年大学习：江山就是人民，人民就是江山'
        self.url = "https://h5.cyol.com/special/daxuexi/byw1m1kn1s/m.html?t=1&z=201",
        self.org_id = 172442  #"北京市海淀团区委"
        self.end_img_url = 'https://h5.cyol.com/special/daxuexi/byw1m1kn1s/images/end.jpg'  #example
        self.study_url = "https://m.bjyouth.net/dxx/check?id=%s&org_id=%s" % (
            self.id, self.org_id)

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
            self.study_url = "https://m.bjyouth.net/dxx/check?id=%s&org_id=%s" % (
                self.id, self.org_id)
            print('update success')
            return 1
        except:
            print('update fail')
            return 0


class Youth():
    def __init__(self, course: QNDXX_NEW_COURSE) -> None:
        self.cookies = ''
        self.username = ''
        self.password = ''
        self.get_cookies_turn = 5
        self.course = course
        self.ua="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6303004c)"
        self.headers = {
            "Host": "m.bjyouth.net",
            "User-Agent":self.ua,
            "Cookie": '',
            "Referer": "https://m.bjyouth.net/qndxx/index.html"
        }
        self.send_message_url = ''
        # example

    # def get_login_cookie_with_selenium(self):

    #     ff_op = webdriver.FirefoxOptions()
    #     ff_op.set_headless()
    #     driver = webdriver.Firefox(firefox_options=ff_op)
    #     # driver=webdriver.PhantomJS() --> cannot work with captcha
    #     driver.get('https://m.bjyouth.net/site/login')

    #     try:
    #         # cap=driver.find_element_by_id('verifyCode-image')
    #         cap = WebDriverWait(driver, 10).until(
    #             EC.presence_of_element_located((By.ID, "verifyCode-image")))
    #         ocr = DdddOcr()
    #         res = ocr.classification(cap.screenshot_as_png)
    #         print(res)

    #         driver.find_element_by_id("username").send_keys(self.username)
    #         driver.find_element_by_id("password").send_keys(self.password)
    #         driver.find_element_by_id("verifyCode").send_keys(res)
    #         driver.find_element_by_tag_name('button').click()
    #         rtn = driver.get_cookie('PHPSESSID')
    #         driver.quit()
    #         return rtn['value']
    #     except:
    #         driver.quit()
    #         return 0

    def get_cookie(self):
        for i in range(self.get_cookies_turn):
            # cookies = self.get_login_cookie_with_selenium()
            cookies=self.get_cookie_with_requests()
            if cookies:
                self.cookies = 'PHPSESSID=' + cookies
                self.headers["Cookie"] = self.cookies
                return 1
        return 0

    def encrpt(self, password, public_key=''):
        if public_key == '':
            public_key = "-----BEGIN PUBLIC KEY-----\nMIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQD5uIDebA2qU746e/NVPiQSBA0Q3J8/G23zfrwMz4qoip1vuKaVZykuMtsAkCJFZhEcmuaOVl8nAor7cz/KZe8ZCNInbXp2kUQNjJiOPwEhkGiVvxvU5V5vCK4mzGZhhawF5cI/pw2GJDSKbXK05YHXVtOAmg17zB1iJf+ie28TbwIDAQAB\n-----END PUBLIC KEY-----"
        rsakey = RSA.importKey(public_key)
        cipher = Cipher_pksc1_v1_5.new(rsakey)
        cipher_text = b64encode(cipher.encrypt(password.encode()))
        return cipher_text.decode()

    def get_cookie_with_requests(self):
        # try:
        if(1):
            S = requests.Session()
            headers = {
                "Host":
                "m.bjyouth.net",
                "User-Agent":
                self.ua
                }
            r = S.get(url="https://m.bjyouth.net/site/login",
                    headers=headers,
                    timeout=5
                    )
            # print(r.status_code)
            r.status_code
            cap_url = "https://m.bjyouth.net" + findall(
                r'src="/site/captcha.+" alt=', r.text)[0][5:-6]
            headers["Referer"] = "https://m.bjyouth.net/site/login"
            cap = S.get(url=cap_url, headers=headers, timeout=5)
            cap.status_code
            ocr = DdddOcr()
            cap_text = ocr.classification(cap.content)
            print(cap_text)
            _csrf_mobile = S.cookies.get_dict()['_csrf_mobile']
            headers['Origin'] = "https://m.bjyouth.net"
            login_username = self.encrpt(self.username)
            login_password = self.encrpt(self.password)
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
        # except:
        #     return 0

    def send_message(self, message: str):
        if self.send_message_url == '':
            return 2
        try:
            url = self.send_message_url % message
            r = requests.get(url, timeout=5)
            r.status_code
            return 1
        except:
            return 0

    def read_config(self, config_path="config.json"):
        with open(config_path, 'r') as f:
            config = json.load(f)
        self.username = config['username']
        self.password = config['password']
        self.send_message_url = config['message_url']

    def study(self):
        # url = "https://m.bjyouth.net/dxx/check?id=%s&org_id=%s" % (
        #     self.course.id, self.course.org_id)
        try:
            r = requests.get(self.course.study_url, self.headers, timeout=5)
            r.status_code
            print('study complete')
            raw_message = "id=%s,%s learned\nend.jpg\n%s\nstudy url:\n%s" % (
                self.course.id, self.course.title[6:10] + '...',
                self.course.end_img_url, self.course.study_url)
            message = requests.utils.quote(raw_message)
            try:
                self.send_message(message)
            except:
                print('send message fail')
            return 1
        except:
            print('study fail')
            return 0


def main():
    print('Start')
    course = QNDXX_NEW_COURSE()
    youth = Youth(course)
    youth.read_config()
    if not youth.get_cookie():
        print('get cookie error')
        return 0
    print('get cookie')
    if not course.update(youth.headers):
        print('update index error')
        return 0
    if not youth.study():
        return 0
    return 1


if __name__ == '__main__':
    main()
