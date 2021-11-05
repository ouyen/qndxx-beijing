from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import json
# import time
# from datetime import date
import requests
from ddddocr import DdddOcr
# import base64


class QNDXX_NEW_COURSE():
    def __init__(self) -> None:
        self.id = 59
        self.title = '青年大学习：江山就是人民，人民就是江山'
        self.url = "https://h5.cyol.com/special/daxuexi/byw1m1kn1s/m.html?t=1&z=201",
        self.org_id = 172440  #"北京市东城团区委"
        self.end_img_url = 'https://h5.cyol.com/special/daxuexi/byw1m1kn1s/images/end.jpg'  #example
        self.study_url= "https://m.bjyouth.net/dxx/check?id=%s&org_id=%s" % (
            self.id, self.org_id
            )

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
            self.org_id = index['rank'][0]['data'][1]['org_id']
            i = self.url.find("/m.html")
            self.end_img_url = self.url[:i] + '/images/end.jpg'
            self.study_url= "https://m.bjyouth.net/dxx/check?id=%s&org_id=%s" % (
                self.id, self.org_id
                )
            print('update success')
            return 1
        except:
            print('update fail')
            return 0


class QNDXX():
    def __init__(self, course: QNDXX_NEW_COURSE) -> None:
        self.cookies = ''
        self.username = ''
        self.password = ''
        self.get_cookies_turn = 5
        self.course = course
        self.headers = {
            "Host": "m.bjyouth.net",
            "User-Agent":
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 NetType/WIFI MicroMessenger/7.0.20.1781(0x6700143B) WindowsWechat(0x6303004c)",
            "Cookie": '',
            "Referer": "https://m.bjyouth.net/qndxx/index.html"
        }
        self.send_message_url = ''
        # example

    def get_login_cookie_with_selenium(self):

        ff_op = webdriver.FirefoxOptions()
        ff_op.set_headless()
        driver = webdriver.Firefox(firefox_options=ff_op)
        # driver=webdriver.PhantomJS() --> cannot work with captcha
        driver.get('https://m.bjyouth.net/site/login')

        try:
            # cap=driver.find_element_by_id('verifyCode-image')
            cap = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "verifyCode-image")))
            ocr = DdddOcr()
            res = ocr.classification(cap.screenshot_as_png)
            print(res)

            driver.find_element_by_id("username").send_keys(self.username)
            driver.find_element_by_id("password").send_keys(self.password)
            driver.find_element_by_id("verifyCode").send_keys(res)
            driver.find_element_by_tag_name('button').click()
            rtn = driver.get_cookie('PHPSESSID')
            driver.quit()
            return rtn['value']
        except:
            driver.quit()
            return 0

    def get_cookie(self):
        for i in range(self.get_cookies_turn):
            cookies = self.get_login_cookie_with_selenium()
            if cookies:
                self.cookies = 'PHPSESSID='+cookies
                self.headers["Cookie"] = self.cookies
                return 1
        return 0

    def send_message(self, message: str):
        if self.send_message_url == '':
            return 2
        try:
            url = self.send_message_url % message
            r=requests.get(url, timeout=5)
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

    def learn_dxx(self):
        # url = "https://m.bjyouth.net/dxx/check?id=%s&org_id=%s" % (
        #     self.course.id, self.course.org_id)
        try:
            r = requests.get(self.course.study_url, self.headers, timeout=5)
            r.status_code
            print('learn complete')
            raw_message = "id=%s,%s learned\nend.jpg\n%s\nstudy url:\n%s" % (
                self.course.id, self.course.title[6:10]+'...', self.course.end_img_url,self.course.study_url)
            message=requests.utils.quote(raw_message)
            try:
                self.send_message(message)
            except:
                print('send message fail')
            return 1
        except:
            print('learn fail')
            return 0


def main():
    print('Start')
    course = QNDXX_NEW_COURSE()
    youth = QNDXX(course)
    youth.read_config()
    if not youth.get_cookie():
        print('get cookie error')
        return 0
    print('get cookie')
    if not course.update(youth.headers):
        print('update index error')
        return 0
    if not youth.learn_dxx():
        return 0
    return 1


if __name__ == '__main__':
    main()
