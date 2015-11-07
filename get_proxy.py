# -*- coding: utf-8 -*-
__author__ = 'admin'
import urllib2
from lagou_db import LagouDb
import bs4
import requests
import re
import threading
import time
import random


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

def get_getproxy(page='1'):
    url = 'http://www.getproxy.jp/en/china/' + str(page)
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


class ProxyCheck(threading.Thread):
    def __init__(self, proxyList, valid_proxy):
        threading.Thread.__init__(self)
        self.proxyList = proxyList
        self.timeout = 5
        self.testUrl = 'http://www.baidu,com/'
        self.valid_proxy = valid_proxy

    def checkProxy(self):
        cookies = urllib2.HTTPCookieProcessor()
        # valid_proxy = []
        for proxy in self.proxyList:
            proxyHandler = urllib2.ProxyHandler({proxy['type']: proxy['ip']})
            # proxyHandler = urllib2.ProxyHandler({'http': '115.29.169.182:37711'})
            opener = urllib2.build_opener(cookies, proxyHandler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]
            t1 = time.time()
            try:
                req = opener.open('http://site.baidu.com/', timeout=self.timeout)
                result = req.read()
                timeused = time.time() - t1
                pos = result.find('030173')
                if pos > 1:
                    self.valid_proxy.append(proxy['ip'])
                    print 'get pos', proxy['ip'], time.time()
                else:
                    print 'not pos', proxy['ip'], time.time()
                    continue
            except Exception, e:
                print 'fail', proxy['ip'], time.time()

    def run(self):
        self.checkProxy()

if __name__ == "__main__":
    valid_proxy = []
    ti = time.time()
    checkThreads = []
    proxy_list = get_getproxy()
    # for i in range(2, 5):
    #     proxy_list += get_getproxy(i)
    t_num = 20
    for i in range(t_num):
        t = ProxyCheck(proxy_list[i*len(proxy_list)/t_num:(i+1)*len(proxy_list)/t_num])
        checkThreads.append(t)

    for i in range(len(checkThreads)):
        checkThreads[i].start()

    for i in range(len(checkThreads)):
        checkThreads[i].join()
    print '%s thread used time %s' % (t_num, time.time()-ti)
    # print proxy_list

    # db = LagouDb().db()
    # db['proxy'].insert_many(valid_proxy)






