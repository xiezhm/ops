#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import requests
import datetime
import sys
headers = {
    'Content-type': 'application/json;charset=utf-8'
} 

def post_tg(messige):
    token = ""
    chat_id = ""
    url = 'https://api.telegram.org/bot{}/sendMessage'.format(token)
    data = {
        "chat_id": chat_id,
        "parse_mode": "Markdownv2",
        "text": messige
    }
    req = requests.post(url=url, json=data, headers=headers).text
    return req

def query_loki():
    data="{compose_project=\"opt\"}|= \"ERROR\""
    ago2m = (datetime.datetime.now()-datetime.timedelta(minutes=30)).timestamp()
    req = requests.get("http://54.169.254.101:3100/loki/api/v1/query_range?query={}&start={}".format(data,ago2m), headers=headers).json()
    for i in req["data"]["result"]:
        host = i["stream"]["host"]
        container_name = i["stream"]["container_name"]
        for x in (i["values"]):
            values = x[1]
            msg = """
Host: ```{}```
App:```{}```
message: ```{}```
        """
            if values.find("INFO") != -1:
                continue
            else:
                print(post_tg(msg.format(host,container_name,values)))
        
query_loki()  

def nginx_loki():
    date_time = datetime.datetime.now()
    data="topk(10, sum by (xff) (count_over_time({app=\"nginx\"} | json |  __error__=\"\" [2m])))"
    req = requests.get("http://54.169.254.101:3100/loki/api/v1/query?query={}".format(data), headers=headers).json()
    for i in req["data"]["result"]:
        ip=i["metric"]["xff"] 
        sum_mumbers=i["value"][-1]
        msg = """
报警名称: ip 2分钟访问超过500次
告警ip: {}
访问次数: {}
告警时间: {}
        """ 
        if int(sum_mumbers) >= 500:
            m = post_tg(msg.format(ip,sum_mumbers,date_time))
            print(m)

if __name__ == "__main__":
    if sys.argv[1] == "java":
        query_loki()
    elif sys.argv[1] == "nginx":
        nginx_loki()
    else:
        sys.exit(1)

