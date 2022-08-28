import requests
import json


class QNDXX_NEW_COURSE():
    def __init__(self) -> None:
        self.id = 59
        self.title = '青年大学习：江山就是人民，人民就是江山'
        self.url = "https://h5.cyol.com/special/daxuexi/byw1m1kn1s/m.html?t=1&z=201",
        # self.org_id = 172442  #"北京市海淀团区委"
        self.end_img_url = 'https://h5.cyol.com/special/daxuexi/byw1m1kn1s/images/end.jpg'  # example
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
            self.url=self.url[:i]
            self.end_img_url = self.url+ '/images/end.jpg'
            self.study_url = f"https://m.bjyouth.net/dxx/check?id={self.id}&org_id=%s"

            self.write_html()
            print('[INFO] Class updated success')
            return 1
        except:
            print('[ERROR] Class update failed')
            return 0

    def write_html(self):
        text = f'''# 青年大学习(北京)

## 使用方法

1. 在微信内打开本网页 or 复制这些文字到微信(比如文件传输助手)
2. 打开登陆页面进行登录, 登陆后返回此页面: https://m.bjyouth.net/qndxx/index.html
3. 点击这个链接, 即刻学习完成: {self.study_url%'172442'}

(以下为可选项)

+ 点击这个链接, 可以查看学习记录: https://m.bjyouth.net/qndxx/index.html#/pages/home/studyrecord

+ 点击这个链接, 可以查看学习成功的截图: {self.end_img_url}

## 本期课程信息

主题为: {self.title}

学习的地址为: {self.url+"/m.html"}

## 风险自负!!!

'''
        with open('html/index.md', 'w', encoding='utf-8') as f:
            f.write(text)
        print('[INFO] Class html written success')
        return True
