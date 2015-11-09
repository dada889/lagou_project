# -*- coding: utf-8 -*-

from get_jd import *


lagou = LagouDb().db()
proxy_list = []




# checkThreads = []
# # get the proxy list
# for i in range(1, 2):
#     proxy_list += get_getproxy(i)
#
# print 'get %s proxy' % len(proxy_list)
#
# ###########################################################################
# # check proxy
# print 'check proxy\n===================================================='
# t_num = 10
# valid_proxy = {}
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
#
# print '\ndone check proxy, %s valid proxy' % len(valid_proxy)




# ### save valid proxy
# temp = list(valid_proxy.items())
# temp_dict = dict(zip(range(len(temp)), temp))
# v_proxy_db = lagou[u'valid_proxy']
# v_proxy_db.drop()
# v_proxy_db.insert_many([{str(0): temp_dict[iid]} for iid in temp_dict.keys()])

### load valid proxy
v_proxy_db = lagou[u'valid_proxy']
temp = v_proxy_db.find()
valid_proxy = {}
for i in temp:
    valid_proxy[i['0'][0]] = i['0'][1]
###########################################################################
# start crawling jd
print '\nstart crawling\n===================================================='
jd_db = lagou[u'杭州_jd']
jd_db.drop()
cursor = lagou[u'杭州'].find({}, {'positionId': 1})[0:30]
# for i in cursor:
#     all_id.append(i['positionId'])


all_id = iter(cursor)
failed_id = []


# ### test single thread
# id = next(all_id)['positionId']
# t = IterGetJd(id=id, db=jd_db, failed_id=failed_id, valid_proxy=valid_proxy, i=1)
# t.start()

has_next = True
while has_next:
    t_num = 3
    crawlThreads = []
    for i in range(t_num):
        has_next = next(all_id, False)
        if has_next:
            id = has_next['positionId']
            print id
            t = IterGetJd(id=id, db=jd_db, failed_id=failed_id, valid_proxy=valid_proxy, i=i)
            crawlThreads.append(t)
        else:
            break
    r = EliminateProxy(valid_proxy)
    crawlThreads.append(r)

    for i in range(len(crawlThreads)):
        crawlThreads[i].start()

    for i in range(len(crawlThreads)):
        crawlThreads[i].join()

print 'done first crawling, %s failed id' % len(failed_id)


