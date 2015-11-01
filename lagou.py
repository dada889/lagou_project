__author__ = 'dada'

import urllib2
import re
import bs4
import requests
import json
from pymongo import MongoClient
import time


class lagou():

    def __init__(self):
        self.url_main = 'http://www.lagou.com/'
        self.url_city = 'http://www.lagou.com/jobs/list_Python?px=default'
        self.url_jobs = 'http://www.lagou.com/jobs/positionAjax.json?city='
        self.city_list = []
        self.get_city()

    def get_city(self):
        response = urllib2.urlopen(self.url_city)
        web = response.read()
        soup = bs4.BeautifulSoup(web)

        cities = soup.find('div', {'class': 'more more-positions'}).find_all('a')
        for i in cities:
            self.city_list.append(i.text)
        self.city_list = self.city_list[1:-1]

