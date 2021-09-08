#!/usr/bin/env python3

import redis
import sys
import json
def redis_info(host,port):
    passwd=""
    rd = redis.Redis(host=host, password=passwd, port=port ,ssl=True, ssl_ca_certs=False)
    return rd.info()

if __name__ == "__main__":
    if len(sys.argv) == 3:
        host = sys.argv[1]
        port = sys.argv[2]
        print(json.dumps(redis_info(host,port)))
    else:
        sys.exit(1)
