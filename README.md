# Automatic completion the QNDXX in Beijing

## Instructions


1. Install [python](https://www.python.org/) , ~~GeckoDriver,~~  run ``pip3 install -r requirements.txt`` to install requirements.
2. Copy config.example.yaml to config.yaml. Edit config.yaml. (Enter this [website](https://m.bjyouth.net/site/login) to retrieve the account and password. Get your organization id [here](https://m.bjyouth.net/qndxx/index.html#/pages/home/my))
3. run  ``python3 main.py`` to learn QNDXX

## Details

1. ~~Use selenium to log in to [Beijing Communist Youth League's Website](https://m.bjyouth.net/site/login) to get cookies.(use dddocr to recognize the captcha)~~
   
   Get cookies with requests.

2. Use cookies to get the newest course id. (from https://m.bjyouth.net/dxx/index)
3. Send a request to https://m.bjyouth.net/dxx/check?id=50&org_id=172442 to finish learning.(you can visit [org list](https://m.bjyouth.net/org/list) to get org_id)

## Multi-user support

Your ``config.yaml`` should be like this:

```
youth:
- username: '' 
  password: '' 
  org_id: '172442'
  message_url: '' 
  send_message_org_id: '172442'  
# user2
- username: '' 
  password: '' 
  org_id: '172442'
  message_url: '' 
  send_message_org_id: '172442'  
# user3...

```
## Github Actions Support (from https://github.com/ashawkey/autodxx)

### Instructions

1. Clone this repository.
2. Create github secrets (Settings --> Secrets --> New Repository secret):
   * USERNAME: your account username (phone number). Visit [here](https://m.bjyouth.net/site/login) to retrieve.
   * PASSWORD: your account password.
   * ORG_ID: your organization id. Visit [here](https://m.bjyouth.net/qndxx/index.html#/pages/home/my) to retrieve.

3. Edit `.github/workflow/main.yml`.
   * by default it runs at 16:50 on every Sunday, change `cron` if you want to run at a different time.

4. Enable workflow for this repository in Actions.

## TODO

1. ~~Use requests to login.~~
2. ~~Add Multi-user support~~
3. Add mail support.

## Back up plan

In general, it is always possible to go through the normal process in selenium headless mode, but the current method is feasible, so I will not continue to develop it now.


## TAKE YOUR OWN RISK!!!