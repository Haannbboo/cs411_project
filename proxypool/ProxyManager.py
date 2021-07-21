import requests

from ProxyDBConnector import ProxyDB
from proxyFetcher import ProxyFetcher


class ProxyManager:

    def __init__(self, proxyDatabase):
        
        self.poolWebsites = None
        self.poolDB = proxyDatabase
        self.fetcher = ProxyFetcher()
        

    def fetchProxy(self):
        proxies = self.fetcher.fetch('66ip', 'http://www.66ip.cn/nmtq.php?getnum=10&isp=0&anonymoustype=0&start=&ports=&export=&ipaddress=&area=1&proxytype=2&api=66ip')
        return proxies


    def checkProxy(self, proxy):
        proxy = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy
            }
        try:
            r = requests.get('http://icanhazip.com', timeout = 5, proxies = proxy)
            response = r.text.strip('\n')
        except requests.exceptions.ProxyError:
            return False
        except requests.exceptions.ConnectTimeout:
            print("Timeout")
            return False
        except requests.exceptions.ReadTimeout:
            print("Timeout")
            return False
        except Exception:
            print("Exception")
            return False
        print(response)
        return response == proxy


    def storeProxy(self, proxy, source):

        self.poolDB.insert(proxy, source)

    def main(self):
        source = '89ip'
        proxies = self.fetchProxy()
        print('here')
        for proxy in proxies:
            if self.checkProxy(proxy):
                print(proxy)
                self.storeProxy(proxy, '89ip')
                
