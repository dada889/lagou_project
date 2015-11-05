# -*- coding: utf-8 -*-
__author__ = 'admin'
import urllib2
import pymongo
import bs4
import requests
import re
import threading
import time
import random

url = 'http://www.freeproxylists.net/zh/'
proxyDict = {'http': 'http://115.29.169.182:37711'}
payload = {'c': 'CN', 'u': 90, 'page': '1'}
# header = {'cookie': 'OTZ=3036000_24_24__24_; PREF=ID=1111111111111111:FF=0:TM=1444790517:LM=1444790517:V=1:S=mQEatvdig0QZQ7Eo; NID=73=tgl8dfoWhmbVIp7fFLDjYqtwBeeyocbaOXBxK8ALE16rBjPy12VQODsvMbED9GhzTbdxK5nIYY7TCay-lSxfwbkMJ4iDgYO36aMwQ0FDKMiMuAJpfHYUrfl-RRvhN6Dbpin4MhlPfJWLrvSnhsv-bikp086BpYgqFEfrup9vNB8K5AbYdxkfU3U2s4RW_w-uBQ'}
r = requests.get(url, proxies=proxyDict, params=payload)
content = r.content
print content
soup = bs4.BeautifulSoup(content)

url1 = 'http://www.freeproxylists.net/zh/'

url2 = 'http://cn-proxy.com/'

# url3 = 'http://www.freeproxylists.net/zh/cn.html'

def get_cn_proxy():
    url = 'http://cn-proxy.com/'
    proxy = urllib2.ProxyHandler({'http': '115.29.169.182:37711'})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    response = urllib2.urlopen(url)
    web = response.read()
    soup = bs4.BeautifulSoup(web)
    proxy_list = []
    table_body = soup.find_all('table',  {'class': 'sortable'})[1].find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        rows_list = re.split('\n+', row.text.strip('\n+'))
        proxy = {}
        proxy['ip'] = rows_list[0] + ':' + rows_list[1]
        proxy['update_time'] = rows_list[3]
        proxy['type'] = 'http'
        proxy_list.append(proxy)
    return proxy_list

def get_getproxy():
    url = 'http://www.getproxy.jp/en/china/1'
    proxy = urllib2.ProxyHandler({'http': '115.29.169.182:37711'})
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    response = urllib2.urlopen(url)
    web = response.read()
    soup = bs4.BeautifulSoup(web)
    table = soup.find('table', {'class': 'mytable'}).find_all('tr')
    proxy_list = []
    for row in table[1:-1]:
        proxy = {}
        elements = row.text.strip('\n').split('\n')
        proxy['ip'] = elements[0]
        proxy['update_time'] = elements[-1]
        proxy['type'] = elements[-2]
        proxy_list.append(proxy)
    return proxy_list


proxy = urllib2.ProxyHandler({'http': '218.244.132.2:37711'})
opener = urllib2.build_opener(proxy)
urllib2.install_opener(opener)
response = urllib2.urlopen('http://www.google,com')

import urllib2
cookies = urllib2.HTTPCookieProcessor()
proxy = urllib2.ProxyHandler({'http': '218.244.132.2:37711'})
opener = urllib2.build_opener(cookies, proxy)
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]
req = opener.open('http://site.baidu.com/', timeout=5)
result = req.read()
print result.find('030173')

proxy1 = get_getproxy()
proxy1 = get_cn_proxy()
for proxy in proxy1:
    cookies = urllib2.HTTPCookieProcessor()
    proxyHandler = urllib2.ProxyHandler({proxy['type']: proxy['ip']})
    # proxyHandler = urllib2.ProxyHandler({'http': '115.29.169.182:37711'})
    opener = urllib2.build_opener(cookies, proxyHandler)
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]
    t1 = time.time()
    try:
        req = opener.open('http://site.baidu.com/', timeout=5)
        result = req.read()
        timeused = time.time() - t1
        pos = result.find('030173')
        if pos > 1:
            print 'get pos', proxy['ip']
        else:
            print 'not pos', proxy['ip']
            continue
    except Exception, e:
        print 'fail', proxy['ip']



class ProxyCheck(threading.Thread):
    def __init__(self, proxyList):
        threading.Thread.__init__(self)
        self.proxyList = proxyList
        self.timeout = 5
        self.testUrl = 'http://www.baidu,com/'

    def checkProxy(selfself):
        cookies = urllib2.HTTPCookieProcessor()
        for proxy in proxy1:
            proxyHandler = urllib2.ProxyHandler({proxy['type']: proxy['ip']})
            # proxyHandler = urllib2.ProxyHandler({'http': '115.29.169.182:37711'})
            opener = urllib2.build_opener(cookies, proxyHandler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]
            t1 = time.time()
            try:
                req = opener.open('http://site.baidu.com/', timeout=5)
                result = req.read()
                timeused = time.time() - t1
                pos = result.find('030173')
                if pos > 1:
                    print 'get pos', proxy['ip']
                else:
                    print 'not pos', proxy['ip']
                    continue
            except Exception, e:
                print 'fail', proxy['ip']





