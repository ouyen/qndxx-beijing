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
            # self.download_img_success=self.download_img()

            self.write_html()
            print('[INFO] Class updated success')
            return 1
        except:
            print('[ERROR] Class update failed')
            return 0

    def download_img(self):
        try:
            r = requests.get(self.end_img_url, timeout=5)
            r.status_code
            with open('html/end.jpg', 'wb') as f:
                f.write(r.content)
            print('[INFO] Class img downloaded success')
            return True
        except:
            print('[ERROR] Class img download failed')
            return False

    def write_html(self):
        text = f'''# 青年大学习(北京)

## 使用方法

1. 在微信内打开本网页 or 复制这些文字到微信(比如文件传输助手)
2. 打开登陆页面进行登录, 登陆后返回此页面: https://m.bjyouth.net/qndxx/index.html
3. 点击这个链接, 即刻学习完成: {self.study_url%'172442'}

(以下为可选项)

+ 点击这个链接, 可以查看学习记录: https://m.bjyouth.net/qndxx/index.html#/pages/home/studyrecord
+ 点击这个链接, 可以查看学习成功的截图: https://ouyen.github.io/qndxx-beijing/end.html
+ 点击这个链接, 可以查看学习成功所显示的图片: {self.end_img_url}

## 本期课程信息

主题为: {self.title}

学习的地址为: {self.url+"/m.html"}

## 风险自负!!!

## star me:

https://github.com/ouyen/qndxx-beijing/

'''
        with open('html/index.md', 'w', encoding='utf-8') as f:
            f.write(text)

        with open('html/end.html', 'w', encoding='utf-8') as f:
            f.write(f'''<!DOCTYPE html>

<html>
    <meta name="referrer" content="never">
    <meta http-equiv="content-type" content="text/html; charset=utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, minimum-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>团课详情</title>
    <style>
    
    </style>
    <img style="position:absolute;left:0px;top:0px;width:100%;height:100%" id="main-img" onerror="onImageLoadError();" src="{self.end_img_url}" referrerpolicy="no-referrer" />

</html>''')
        print('[INFO] Class html written success')
        return True
