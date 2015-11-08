# -*- coding: utf-8 -*-

from get_jd import *


lagou = LagouDb().db()
proxy_list = []
valid_proxy = []
failed_id = []
jd_db = lagou[u'杭州_jd']
all_id = []
cursor = lagou[u'杭州'].find({}, {'positionId': 1})[0:200]
for i in cursor:
    all_id.append(i['positionId'])

checkThreads = []
crawlThreads = []
# get the proxy list
for i in range(1, 3):
    proxy_list += get_getproxy(i)
print 'get %s proxy' % len(proxy_list)