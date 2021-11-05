# Automatic completion the QNDXXX in Beijing

## Instructions

1. Copy config.example.json to config.json
2. Install [python](https://www.python.org/) , [GeckoDriver](https://zhuanlan.zhihu.com/p/33746273) , run ``pip3 install -r requirements.txt`` to install requirements.
3. Edit config.json. (Enter this [website](https://m.bjyouth.net/site/login) to retrieve the account and password)
```
{
    "username":"12345678901",:your phone number
    "password":"qndxxpassword",:your password
    "message_url":"":When learning is complete, requests.get(message_url % message) to send message.If you don't konw what it is,leave it blank 
}
```
4.run  ``python3 main.py`` to learn QNDXX

## TODO

1. Use requests to login.
2. Add mail support.
