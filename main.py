import os


import time
import random

import requests
import yaml


from Youth import Youth


def main(remote_config=""):
    youth = Youth()
    course = youth.course
    print("[INFO] Read config from config.yaml")
    if remote_config:
        print("[INFO] Read remote config")
        try:
            r = requests.get(remote_config, timeout=5)
            r.status_code
            print("[INFO] Get remote config succeed")
            try:
                config_dict = yaml.safe_load(r.text)
            except:
                print("[ERROR] Please check your remote config")
                return 0
        except:
            print("[ERROR] Get remote config failed")
            return 0
    else:
        with open("config.yaml", "r") as f:
            config_dict = yaml.safe_load(f)

    user_i = 0
    for single_config in config_dict["youth"]:
        print("[INFO] User ", user_i, " Start")
        user_i += 1
        youth.read_config(single_config)
        if not youth.get_cookie():
            continue
        if course.need_update:
            if not course.update(youth.headers):
                continue
            course.need_update = False
        if not youth.study():
            continue
        sleep_time = 2 + random.random()
        print(f"[INFO] Sleep {sleep_time} s")
        time.sleep(sleep_time)
    return 1


def main_cli(args):
    print("[INFO] Read config from command line parameters")
    print("[INFO] Start")
    youth = Youth()
    youth.username = args["USERNAME"]
    youth.password = args["PASSWORD"]
    youth.org_id = args["ORG_ID"]
    if not youth.get_cookie():
        return 0
    if not youth.course.update(youth.headers):
        return 0
    if not youth.study():
        return 0


if __name__ == "__main__":
    ENV = {
        _i: os.getenv(_i) for _i in ["PASSWORD", "USERNAME", "ORG_ID", "REMOTE_CONFIG"]
    }
    if ENV["REMOTE_CONFIG"]:
        main(ENV["REMOTE_CONFIG"])
    elif ENV["USERNAME"] and ENV["PASSWORD"] and ENV["ORG_ID"]:
        main_cli(ENV)
    else:
        main()
