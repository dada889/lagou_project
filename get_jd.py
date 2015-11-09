# -*- coding: utf-8 -*-
__author__ = 'dada'

from pymongo import MongoClient
import urllib2
import re
import bs4
import time
import socket
import threading
from lagou_db import LagouDb
from get_proxy import ProxyCheck, get_getproxy

socket.setdefaulttimeout(5)


# proxy = urllib2.ProxyHandler({'http': '180.166.112.47:8888'})
# opener = urllib2.build_opener(proxy)
# url_loader = urllib2
# url_loader.install_opener(opener)
# web = url_loader.urlopen('http://www.lagou.com/', timeout=5)
# text = web.read()


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


# def get_jd(job_id):
#     result = {}
#     url = 'http://www.lagou.com/jobs/' + str(job_id) + '.html'
#     try:
#         response = urllib2.urlopen(url)
#         web = response.read()
#         soup = bs4.BeautifulSoup(web)
#         jd = soup.find('dd', {'class': 'job_bt'})
#         jd_str = jd.text.strip('\s*\n\s*')
#         bs_rela = soup.find('dl', {'class': 'post_again module-container'}).find('ul')
#     except:
#         return job_id
#     details_str = bs_rela.text.strip('\n')
#     details_list = re.split('\.*\s+', details_str)[1:-1]
#     details_list = [i for i in chunks(details_list, 3)]
#     posi_href_list = bs_rela.select('a.position')
#     id_list = [filter(str.isdigit, str(id.attrs['href'])) for id in posi_href_list]
#     result['jd'] = jd_str
#     result['post_again'] = dict(zip(id_list, details_list))
#     return result
#
#
# def go(ip, db_name, collection_name, num=0):
#     client = MongoClient(ip, 27017)
#     db = client[db_name]
#     collection = db[collection_name]
#     colle_jd = db[collection_name + '_jd']
#     successed = []
#     failed = []
#     for i in collection.find({}, {'positionId': 1})[num:]:
#         id = i['positionId']
#         result = get_jd(id)
#         if isinstance(result, dict):
#             colle_jd.insert(result)
#             successed.append(id)
#         else:
#             failed.append(id)
#             print 'fail', id
#         num += 1
#         print 'success', id, 'num', num
#         time.sleep(2)
#     return successed, failed, num


class GetJd(threading.Thread):
    def __init__(self, id_list, db, failed_id, valid_proxy, proxy='180.166.112.47:8888'):
        threading.Thread.__init__(self)
        self.job_id_list = id_list
        self.proxy = proxy
        self.db = db
        self.failed_id = failed_id
        self.valid_proxy = valid_proxy

    def collect_jd(self, time_out=5):
        for id in self.job_id_list:
            result = {}
            try:
                url = 'http://www.lagou.com/jobs/' + str(id) + '.html'
                proxy = urllib2.ProxyHandler({'http': self.proxy})
                opener = urllib2.build_opener(proxy)
                url_loader = urllib2
                url_loader.install_opener(opener)
                web = url_loader.urlopen(url, timeout=time_out).read()
                soup = bs4.BeautifulSoup(web)
                jd = soup.find('dd', {'class': 'job_bt'})
                jd_str = jd.text.strip('\s*\n\s*')
                bs_rela = soup.find('dl', {'class': 'post_again module-container'}).find('ul')
            except:
                self.failed_id.append(id)
                self.valid_proxy[self.proxy] += 1
                print 'failed in proxy %s to get jd in id %s \n with value %s' % (self.proxy, id, self.valid_proxy[self.proxy])
                continue
            details_str = bs_rela.text.strip('\n')
            details_list = re.split('\.*\s+', details_str)[1:-1]
            details_list = [j for j in chunks(details_list, 3)]
            posi_href_list = bs_rela.select('a.position')
            id_list = [filter(str.isdigit, str(id1.attrs['href'])) for id1 in posi_href_list]
            result['positionId'] = id
            result['jd'] = jd_str
            result['post_again'] = dict(zip(id_list, details_list))
            # self.temp.append(result)
            self.db.insert_one(result)
            print 'success in proxy %s in id %s' % (self.proxy, id)

    def run(self):
        self.collect_jd()

class IterGetJd(threading.Thread):
    def __init__(self, id, db, failed_id, valid_proxy, i):
        threading.Thread.__init__(self)
        self.time_out = 5
        self.id = id
        self.proxy = valid_proxy.keys()[i]
        self.db = db
        self.failed_id = failed_id
        self.valid_proxy = valid_proxy
    def get_jd(self):
        result = {}
        url = 'http://www.lagou.com/jobs/' + str(self.id) + '.html'
        # print url
        try:
            proxy = urllib2.ProxyHandler({'http': self.proxy})
            opener = urllib2.build_opener(proxy)
            url_loader = urllib2
            url_loader.install_opener(opener)
            web = url_loader.urlopen(url, timeout=self.time_out).read()
            soup = bs4.BeautifulSoup(web)
            jd = soup.find('dd', {'class': 'job_bt'})
            jd_str = jd.text.strip('\s*\n\s*')
            bs_rela = soup.find('dl', {'class': 'post_again module-container'}).find('ul')
        except:
            self.failed_id.append(id)
            self.valid_proxy[self.proxy] += 1
            print 'failed in proxy %s to get jd in id %s with value %s' % (self.proxy, self.id, self.valid_proxy[self.proxy])
            return ''
        details_str = bs_rela.text.strip('\n')
        details_list = re.split('\.*\s+', details_str)[1:-1]
        details_list = [j for j in chunks(details_list, 3)]
        posi_href_list = bs_rela.select('a.position')
        id_list = [filter(str.isdigit, str(id1.attrs['href'])) for id1 in posi_href_list]
        result['positionId'] = self.id
        result['jd'] = jd_str
        result['post_again'] = dict(zip(id_list, details_list))
        # self.temp.append(result)
        self.db.insert_one(result)
        print 'success in proxy %s in id %s' % (self.proxy, self.id)

    def run(self):
        self.get_jd()


class EliminateProxy(threading.Thread):
    def __init__(self, valid_proxy):
        threading.Thread.__init__(self)
        self.valid_proxy = valid_proxy

    def eliminate(self):
        for proxy in self.valid_proxy.keys():
            if self.valid_proxy[proxy] >= 5:
                print 'remove proxy %s' % proxy
                self.valid_proxy.pop(proxy, None)

    def run(self):
        self.eliminate()







if __name__ == "__main__":
    ############################
    ## test IterGetJd
    ############################
    lagou = LagouDb().db()
    proxy_list = []

    ### load valid proxy
    v_proxy_db = lagou[u'valid_proxy']
    temp = v_proxy_db.find()
    valid_proxy = {}
    for i in temp:
        valid_proxy[i['0'][0]] = i['0'][1]

    jd_db = lagou[u'杭州_jd']
    cursor = lagou[u'杭州'].find({}, {'positionId': 1})[0:20]
    all_id = iter(cursor)
    failed_id = []
    id = next(all_id)['positionId']
    t = IterGetJd(id=id, db=jd_db, failed_id=failed_id, valid_proxy=valid_proxy, i=1)
    t.start()

    # lagou = LagouDb().db()
    # proxy_list = []
    # valid_proxy = []
    # failed_id = []
    # jd_db = lagou[u'杭州_jd']
    # all_id = []
    # cursor = lagou[u'杭州'].find({}, {'positionId': 1})[0:200]
    # for i in cursor:
    #     all_id.append(i['positionId'])
    #
    # checkThreads = []
    # crawlThreads = []
    # # get the proxy list
    # for i in range(1, 3):
    #     proxy_list += get_getproxy(i)
    # print 'get %s proxy' % len(proxy_list)
    #
    # ###########################################################################
    # # check proxy
    # print 'check proxy\n===================================================='
    # t_num = 20
    # for i in range(t_num):
    #     pl = proxy_list[i*len(proxy_list)/t_num:(i+1)*len(proxy_list)/t_num]
    #     t = ProxyCheck(pl, valid_proxy)
    #     checkThreads.append(t)
    #
    # for i in range(len(checkThreads)):
    #     checkThreads[i].start()
    #
    # for i in range(len(checkThreads)):
    #     checkThreads[i].join()
    # # save in mongoprint 'check proxy'
    # # print 'done check proxy, %s valid proxy' % len(valid_proxy)
    # # lagou['proxy'].insert_many(valid_proxy)
    #
    # # valid_proxy_dict = {}
    # # for i in valid_proxy:
    # #     # print i['ip']
    # #     valid_proxy_dict[i] = 0
    # print 'done check proxy, %s valid proxy' % len(valid_proxy)
    # # lagou['proxy'].insert_many(valid_proxy)
    #
    # ###########################################################################
    # # start crawling jd
    # print '\nstart crawling\n===================================================='
    # t_num = 20
    # for i in range(t_num):
    #     idlist = all_id[i * len(all_id) / t_num:(i + 1) * len(all_id) / t_num]
    #     t = GetJd(id_list=idlist, db=jd_db, proxy=valid_proxy.keys()[i])
    #     crawlThreads.append(t)
    #
    # for i in range(len(crawlThreads)):
    #     crawlThreads[i].start()
    #
    # for i in range(len(crawlThreads)):
    #     crawlThreads[i].join()
    #     if valid_proxy_dict[valid_proxy[i]] >= 5:
    #         print 'remove proxy %s' % valid_proxy[i]
    #         valid_proxy.remove(valid_proxy[i])
    #
    #
    #
    #
    # ###########################################################################
    # # start failed id
    # rep_time = 1
    # while (failed_id > 0) & (rep_time <= 3):
    #     all_id = failed_id
    #     failed_id = []
    #     print 'start failed id\n===================================================='
    #     for i in range(t_num):
    #         idlist = all_id[i * len(all_id) / t_num:(i + 1) * len(all_id) / t_num]
    #         t = GetJd(id_list=idlist, proxy=valid_proxy[i])
    #         crawlThreads.append(t)
    #
    #     for i in range(len(crawlThreads)):
    #         crawlThreads[i].start()
    #
    #     for i in range(len(crawlThreads)):
    #         crawlThreads[i].join()
    #         if valid_proxy_dict[valid_proxy[i]] >= 5:
    #             print 'remove proxy %s' % valid_proxy[i]
    #             valid_proxy.remove(valid_proxy[i])
    #     rep_time += 1
    #
    # print 'done'
    # for i in valid_proxy_dict.keys():
    #     print i, valid_proxy_dict[i]