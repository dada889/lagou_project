# -*- coding: utf-8 -*-
__author__ = 'admin'
import urllib2
import pymongo
import bs4
import requests
import re

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

def cn_proxy():
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
        proxy_list.append(proxy)
    return proxy_list


rows = table_body.find_all('tr')
for row in rows:
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data.append([ele for ele in cols if ele]) # Get rid of empty values