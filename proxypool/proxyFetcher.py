import requests
from pyquery import PyQuery as pq


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
        
