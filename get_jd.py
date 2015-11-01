__author__ = 'dada'

from pymongo import MongoClient
import urllib2
import re
import bs4

client = MongoClient('localhost', 27017)
db = client['lagou']
xm = db[u'厦门']

temp = xm.find_one()

# job_list = []
# for data in xm.find():
#     temp = {}
#     print data['positionId']
#     temp['positionId'] = data['positionId']
#     temp['positionName'] = data['positionName']
#     temp['companyId'] = data['companyId']
#     temp['companyName'] = data['companyName']
#     job_list.append(temp)

id = temp['positionId']
url_jd = 'http://www.lagou.com/jobs/' + str(id) + '.html'
response = urllib2.urlopen(url_jd)
web = response.read()
soup = bs4.BeautifulSoup(web)
jd = soup.select('dd.job_bt p')
jd = soup.find('dd', {'class': 'job_bt'})
jd_str = jd.text.strip('\s*\n\s*')

post_again = soup.select('a.position')

bs_rela = soup.find('dl', {'class': 'post_again module-container'}).find('ul')

details_str = bs_rela.text.strip('\s*\n\s*')
details_list = re.split('\.*\s+', details_str)[1:-1]
posi_href_list = bs_rela.select('a.position')
id_list = [filter(str.isdigit, id.attrs['href']) for id in posi_href_list]


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in xrange(0, len(l), n):
        yield l[i:i + n]


def get_jd(job_id):
    result = {}
    url = 'http://www.lagou.com/jobs/' + str(job_id) + '.html'
    response = urllib2.urlopen(url)
    web = response.read()
    soup = bs4.BeautifulSoup(web)
    jd = soup.find('dd', {'class': 'job_bt'})
    jd_str = jd.text.strip('\s*\n\s*')
    bs_rela = soup.find('dl', {'class': 'post_again module-container'}).find('ul')
    details_str = bs_rela.text.strip('\n')
    details_list = re.split('\.*\s+', details_str)[1:-1]
    details_list = [i for i in chunks(details_list, 3)]
    posi_href_list = bs_rela.select('a.position')
    id_list = [filter(str.isdigit, id.attrs['href']) for id in posi_href_list]
    result['jd'] = jd_str
    result['post_again'] = dict(zip([id_list, details_list]))
    return result



