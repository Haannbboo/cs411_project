import requests

from ProxyDBConnector import ProxyDB
from proxyFetcher import ProxyFetcher


class ProxyManager:
    # using a proxy service provider is simple and more stable
    # but the lifespan of a proxy would be about 5min
    # so it might not be necessary to store proxies in the database
    # originally, this was designed to be a proxy pool scanning, checking, and storing IPs

    def __init__(self):

        self.poolWebsites = None
        self.poolDB = ProxyDB('veGryq-roccab-tawsi5')
        self.fetcher = ProxyFetcher()

    def fetchProxy(self):
        proxies = self.fetcher.fetch('mogu',
                                     'http://piping.mogumiao.com/proxy/api/get_ip_bs?appKey=8bba97f819114c34a8fffea71bff211e&count=5&expiryDate=0&format=1&newLine=2')
        return proxies

    def checkProxy(self, proxy):
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy
        }
        try:
            r = requests.get('http://icanhazip.com', timeout=5, proxies=proxies)
            response = r.text.strip('\n')
        except requests.exceptions.ProxyError:
            print("ProxyError")
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
        # print(response)
        return response == proxy.split(':')[0]

    def storeProxy(self, proxy, source):

        self.poolDB.insert(proxy, source)

    def main(self):
        source = 'mogu'
        proxies = self.fetchProxy()
        print(len(proxies))
        for proxy in proxies:
            if self.checkProxy(proxy):
                print(proxy)
                # self.storeProxy(proxy, 'mogu')

    def getProxy(self):
        # scratch
        proxy = ""
        if self.checkProxy(proxy):
            # proxy ip is working
            return proxy
        else:
            # proxy ip not working
            return
