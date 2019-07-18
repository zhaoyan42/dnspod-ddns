import re
import logging
import socket
import json
from urllib import request, error, parse

# 匹配合法 IP 地址
regex_ip = re.compile(
    r"\D*("
    + r"(?:1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\."
    + r"(?:1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\."
    + r"(?:1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\."
    + r"(?:1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)"
    + r")\D*")

# 增强鲁棒性，用多种方式获取 IP
def get_ip():
    return (get_ip_by_taobao()
        or  get_ip_by_ipip()
        or  get_ip_by_httpbin()
        or  get_ip_by_httpbin_direct_1() )
    
# 这几个函数会在 DNS 遭受污染时失效
def get_ip_by_taobao():
    url = 'http://ip.taobao.com/service/getIpInfo.php?ip=myip'
    try:
        resp = request.urlopen(url=url, timeout=10).read()
        jsonBody = json.loads(resp.decode("utf-8"))
        ip = jsonBody['data']['ip']
        logging.info("get ip by taobao: %s" % ip)
        return ip
    except Exception as e:
        logging.warning("get_ip_by_taobao FAILED, error: %s", str(e))
        return None

def get_ip_by_ipip():
    url = 'http://myip.ipip.net/'
    try:
        resp = request.urlopen(url=url, timeout=10).read()
        ip = regex_ip.match(resp.decode("utf-8")).group(1)
        logging.info("get ip by ipip: %s" % ip)
        return ip
    except Exception as e:
        logging.warning("get_ip_by_ipip FAILED, error: %s", str(e))
        return None

def get_ip_by_httpbin():
    url = 'http://www.httpbin.org/ip'
    try:
        resp = request.urlopen(url=url, timeout=10).read()
        ip = regex_ip.match(resp.decode("utf-8")).group(1)
        logging.info("get ip by httpbin: %s" % ip)
        return ip
    except Exception as e:
        logging.warning("get_ip_by_httpbin FAILED, error: %s", str(e))
        return None

# 这个函数可以在本地 DNS 遭受污染的时候获取到IP
# 如需模拟DNS污染，可以在HOSTS文件里加入 127.0.0.1 www.httpbin.org
def get_ip_by_httpbin_direct_1():
    url = 'http://52.201.109.155/ip'
    try:
        req = request.Request(url=url, method='GET', headers={'Host': 'www.httpbin.org'})
        resp = request.urlopen(req).read()
        ip = regex_ip.match(resp.decode("utf-8")).group(1)
        logging.info("get ip by httpbin_direct_1: %s" % ip)
        return ip
    except Exception as e:
        logging.warning("get_ip_by_httpbin_direct_1 FAILED, error: %s", str(e))
        return None

    
# 测试
if __name__ == '__main__':
    print(get_ip()                     )
    print(get_ip_by_taobao()             )
    print(get_ip_by_ipip()             )
    print(get_ip_by_httpbin()          )
    print(get_ip_by_httpbin_direct_1() )