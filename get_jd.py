__author__ = 'dada'

from pymongo import MongoClient
import urllib2
import re
import bs4
import time




# job_list = []
# for data in xm.find():
#     temp = {}
#     print data['positionId']
#     temp['positionId'] = data['positionId']
#     temp['positionName'] = data['positionName']
#     temp['companyId'] = data['companyId']
#     temp['companyName'] = data['companyName']
#     job_list.append(temp)

# id = temp['positionId']
# url_jd = 'http://www.lagou.com/jobs/' + str(id) + '.html'
# response = urllib2.urlopen(url_jd)
# web = response.read()
# soup = bs4.BeautifulSoup(web)
# jd = soup.select('dd.job_bt p')
# jd = soup.find('dd', {'class': 'job_bt'})
# jd_str = jd.text.strip('\s*\n\s*')
#
# post_again = soup.select('a.position')
#
# bs_rela = soup.find('dl', {'class': 'post_again module-container'}).find('ul')
#
# details_str = bs_rela.text.strip('\s*\n\s*')
# details_list = re.split('\.*\s+', details_str)[1:-1]
# posi_href_list = bs_rela.select('a.position')
# id_list = [filter(str.isdigit, id.attrs['href']) for id in posi_href_list]


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def get_jd(job_id):
    result = {}
    url = 'http://www.lagou.com/jobs/' + str(job_id) + '.html'
    try:
        response = urllib2.urlopen(url)
        web = response.read()
        soup = bs4.BeautifulSoup(web)
        jd = soup.find('dd', {'class': 'job_bt'})
        jd_str = jd.text.strip('\s*\n\s*')
        bs_rela = soup.find('dl', {'class': 'post_again module-container'}).find('ul')
    except:
        return job_id
    details_str = bs_rela.text.strip('\n')
    details_list = re.split('\.*\s+', details_str)[1:-1]
    details_list = [i for i in chunks(details_list, 3)]
    posi_href_list = bs_rela.select('a.position')
    id_list = [filter(str.isdigit, str(id.attrs['href'])) for id in posi_href_list]
    result['jd'] = jd_str
    result['post_again'] = dict(zip(id_list, details_list))
    return result


desktop = MongoClient('localhost', 27017)
d_lagou = desktop['lagou']
d_test = d_lagou[u'test']
d_test_jd = d_lagou['test_jd']
d_test_mis = d_lagou['test_mis']


thinkpad = MongoClient('192.168.1.18', 27017)
t_lagou = thinkpad['lagou']
t_test = t_lagou['test']

# temp = d_test.find_one()
# result = get_jd(temp['positionId'])
# isinstance(temp_jd, dict)
# d_test_jd.insert(result)


def go(ip, db_name, collection_name, num=0):
    client = MongoClient(ip, 27017)
    db = client[db_name]
    collection = db[collection_name]
    colle_jd = db[collection_name+'_jd']
    successed = []
    failed = []
    for i in collection.find({}, {'positionId': 1})[num:]:
        id = i['positionId']
        result = get_jd(id)
        if isinstance(result, dict):
            colle_jd.insert(result)
            successed.append(id)
        else:
            failed.append(id)
            print 'fail', id
        num += 1
        print 'success', id, 'num', num
        time.sleep(2)
    return successed, failed, num

s = []
f = []
s, f, n = go('localhost', 'lagou', 'test', 180)

