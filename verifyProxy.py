import json
import os

import requests

proxyFile = "C:\\Users\\小豆\\Desktop\\Proxies2023-02-04.txt"
url = "https://www.baidu.com/"
file = open(proxyFile)
https = []
# file.readline().replace('\r', '').replace('\n', '')
for line in file:
    line = line.strip()
    try:
        resp = requests.get(url=url, proxies={
            "http": "http://" + line,
            "https": "https://" + line
        }, verify=False,timeout=30)
        https.append(line)
        print(line + "yes")
    except Exception as e:
        print(e)
        print(line + "not")
print(json.dumps(https))
