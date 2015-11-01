# -*- coding: utf-8 -*-
__author__ = 'dada'

import urllib2
import re
import bs4
import requests
import json
from pymongo import MongoClient
import time

############################################################################################
# get all category
############################################################################################
response = urllib2.urlopen("http://www.lagou.com/")
web = response.read()

soup = bs4.BeautifulSoup(web)
menu_main = soup.select('div.menu_main a')
menu_sub = soup.select('div.menu_sub a')
# print len(menu_main)
# print len(menu_sub)



menu_sub_dict = {}
for i in menu_sub:
    name = i.text.strip()
    url = i.attrs['href'].strip()
    tj_id = i.attrs['data-lg-tj-id'].strip()
    tj_no = i.attrs['data-lg-tj-no'].strip()
    menu_sub_dict[name] = [url, tj_id, tj_no]

# for i in sorted(menu_sub_dict.keys()):
#     print i



############################################################################################
# get city name
############################################################################################

# city_url = 'http://www.lagou.com/jobs/list_Python?px=default&city=%E5%85%A8%E5%9B%BD'
# response = urllib2.urlopen(city_url)
# web = response.read()
# soup = bs4.BeautifulSoup(web)
#
# cities = soup.find('div', {'class': 'more more-positions'}).find_all('a')
#
# city_list = []
# for i in cities:
#     city_list.append(i.text)
# city_list = city_list[1:-1]

############################################################################################
# get all job url
############################################################################################


def get_job_link(city, kd):
    data = []
    url = 'http://www.lagou.com/jobs/positionAjax.json?city=' + city
    n = 1
    n_job = 100
    # kd = 'Python'
    while (n_job >= 15):
        if n == 1:
            payload = {'first': 'true', 'pn': n, 'kd': kd}
            r = requests.post(url, data=payload)
        else:
            payload = {'first': 'false', 'pn': n, 'kd': kd}
            r = requests.post(url, data=payload)
        print 'page:', n, 'status code', r.status_code
        r_json = r.json()
        raw_txt = r.text
        json_txt = json.loads(raw_txt)
        json_content = json_txt['content']
        # print json_content['totalPageCount']
        result = json_content['result']
        n_job = len(result)
        print 'job url:', len(result), kd
        n += 1
        data += result
        time.sleep(2)
    print 'end', n
    return data

def mongo_insert(data, db_name, cl_name, one=False):
    client = MongoClient('localhost', 27017)
    db = client[db_name]
    collection = db[cl_name]
    if not one:
        collection.insert_many(data)
    else:
        collection.insert_one(data)

type_list = sorted(menu_sub_dict.keys())
for i in type_list:
    data = get_job_link(u'深圳', i)
    print 'finish', i, 'dumping into database'
    if data:
        mongo_insert(data, 'lagou', u'深圳')










