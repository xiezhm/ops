#!/bin/env python3
# -*- coding:utf-8-*-
import requests
import datetime
import os

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    "accept": "application/json, text/plain, */*",
    'Content-Type': 'application/json;charset=utf-8'}


def web(website):
    req_status = requests.get(website, headers=headers, timeout=2).status_code
    # print(type(req_status), req_status)
    if req_status is not 200:
        return website + "域名访问不正常"


def web_ssl(website):
    os.system("curl -o /dev/null --trace /tmp/trace.txt -s   --connect-timeout 2  " + website)
    with open("/tmp/trace.txt") as f:
        b = f.readlines()
        for i in b:
            if "== Info:  expire date:" in i:
                end_time = i.split("expire date: ")[1][0:-5]
                data_end = datetime.datetime.strptime(str(end_time), '%b %d %H:%M:%S %Y')
                if data_end < datetime.datetime.now() + datetime.timedelta(days=15):
                    return website + " https证书少于15天,要过期了!"


def post(token, chat_id, message):
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
    data = {
        "chat_id": chat_id,
        "parse_mode": "Markdown",
        "text": message
    }
    req = requests.post(url=url, json=data, headers=headers).text
    return req


websites = ["https://www.baidu.com", "https://sogo.com"]

if __name__ == "__main__":
    token = ""
    chat_id = ""
    message = []
    for website in websites:
        web_status = web(website=website)
        web_https = web_ssl(website=website)
        if web_status is not None:
            message.append(web_status)
        elif web_https is not None:
            message.append(web_https)
    data = """
    {}
    """
    a = post(token=token, chat_id=chat_id, message=data.format(message))
    print(a)
