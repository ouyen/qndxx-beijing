# Automatic completion the QNDXX in Beijing

## Instructions

1. Copy config.example.json to config.json
2. Install [python](https://www.python.org/) , ~~[GeckoDriver](https://github.com/mozilla/geckodriver/releases) ( [instructions from zhihu](https://zhuanlan.zhihu.com/p/33746273) ),~~  run ``pip3 install -r requirements.txt`` to install requirements.
3. Edit config.json. (Enter this [website](https://m.bjyouth.net/site/login) to retrieve the account and password)
```
{
    "youth": [
        {
            "username": "",--your phone number
            "password": "",--your password
            "org_id": "",-- your organization id (default 172442)
            "message_url": "",--When the study is over, requests.get(message_url % message) to send message.If you don't konw what it is,leave it blank. 
            "send_message_org_id":""-- you can change this to change the org_id in message.(default 172442,blank means same as org_id)
        }
    ]
}
```
4.run  ``python3 main.py`` to learn QNDXX

## Details

1. ~~Use selenium to log in to [Beijing Communist Youth League's Website](https://m.bjyouth.net/site/login) to get cookies.(use dddocr to recognize the captcha)~~
   
   Get cookies with requests.

2. Use cookies to get the newest course id. (from https://m.bjyouth.net/dxx/index)
3. Send a request to https://m.bjyouth.net/dxx/check?id=50&org_id=172442 to finish learning.(you can visit [org list](https://m.bjyouth.net/org/list) to get org_id)


## TODO

1. ~~Use requests to login.~~
2. ~~Add Multi-user support~~
3. Add mail support.

## Back up plan

In general, it is always possible to go through the normal process in selenium headless mode, but the current method is feasible, so I will not continue to develop it now.

## TAKE YOUR OWN RISK!!!