#!/usr/bin/env python3
import requests
import sys


def service(url, data):
    """
    :param url: http://172.18.0.31:8070/user/selectByPhone
    :param data: phone=18566683527
    :return: status_code
    """
    status_code = requests.get(url, data, timeout=3).status_code
    print(status_code, end='')


if __name__ == '__main__':
    url = sys.argv[1]
    parameter1 = sys.argv[2]
    parameter2 = sys.argv[3]
    data = {}

    def pd(s):
        l = s.split("=")
        data[l[0]] = l[1]
    pd(parameter1)
    pd(parameter2)
    service(url, data)

