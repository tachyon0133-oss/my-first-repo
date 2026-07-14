import os
import requests

LOGIN_URL = "https://regist.netkeiba.com/"


def login():

    session = requests.Session()

    email = os.getenv("NETKEIBA_EMAIL")
    password = os.getenv("NETKEIBA_PASSWORD")

    #
    # ここは後で実際のPOST内容を確認して実装
    #

    return session
