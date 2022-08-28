import requests
import json

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
