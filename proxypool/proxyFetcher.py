import requests
from pyquery import PyQuery as pq
import json


class ProxyFetcher:

    def __init__(self):

        self.sources = None


    def fetch(self, source, url):
        
        if source == '89ip':
            html = requests.get(url).text
            doc = pq(html)
            proxies = doc.text().split('\n')[1: -1]
            return proxies

        if source == '66ip':
            html = requests.get(url).text
            doc = pq(html)
            proxies = doc.text().split('\n')[2: -2]
            return proxies

        if source == 'mogu':
            html = requests.get(url).text
            content = json.loads(html)
            if content['code'] == '0':
                proxies = [ip['ip'] + ':' + ip['port'] for ip in content['msg']]
                return proxies
            else:
                return []  # when error code
