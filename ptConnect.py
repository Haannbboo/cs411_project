from pyppeteer import launch
import datetime
import asyncio
import parse

from ConnectParent import Connector



class pyppeteer_connection(Connector):
    # each connection corresponds to a proxy ip
    # each ip would survive for couple searches
    # proxy: 123.123.123.123:1234

    def __init__(self, proxy):
        self.proxy = proxy

        self.url_mainPage = "https://ctrip.com"
        self.template_url = 'https://flights.ctrip.com/international/search/oneway-{C1}-{C2}?depdate={T}'

        self.pages = []
        self.CTs = []

        self.currPage = None
        self.currCT = None

        Connector.__init__(self)

    
    async def create_browser(self):
        self.browser = await launch(headless=True, args=['--disable-infobars', '--proxy-server={}'.format(self.proxy)])
    
    async def close_browser(self):
        await self.browser.close()

    async def new_page(self, url=None, goto_or_not=True):
        # go to page with url

        if url is None:
           self.currPage = await self.browser.newPage()
           self.pages.append(currPage)
           self.currCT = None
           self.CTs.append(None)

        if goto_or_not is True: 
            tempPage = await self.browser.newPage()

            await tempPage.setUserAgent(self._choose_user_agent())
            
            await page.evaluateOnNewDocument('() =>{ Object.defineProperties(navigator, { webdriver:{ get: () => false } }) }')

            await tempPage.goto(url, {'waitUntil': 'load'})

            self.pages.append(tempPage)
            self.currPage = tempPage
            self.currCT = self._convert_url_CT(url)
            self.CTs.append(self.currCT)

        else:
            # click on the page
            tabs = await self.currPage.querySelectorAll('.calendarlp-tab .tabs-content li.tab')
            tabs = tabs[7:13]
            for tab in tabs:
                date = await tab.querySelector('.date')

    
    async def close_page(self):
        # close currPage
        if self.currPage is None:
            return
        
        await self.currPage.close()
        
        if len(self.pages) == 1:
            assert len(self.CTs) == 1
            self.currPage = None
            self.pages.pop()
            self.currCT = None
            self.CTs.pop()
        else:
            self.pages.pop()
            self.currPage = self.pages[-1]
            self.CTs.pop()
            self.currCT = self.CTs[-1]
            assert len(self.currPage) == len(self.CTs)


    
    async def check_tickets(self, CT):
        # main func

        url = self._convert_CT_url(CT)
        goto_or_not = self._need_goto_page(CT)

        await self.new_page(url, goto_or_not)

        result = await self.parse_page()
        self.send_to_processing(result)

        if goto_or_not:
            await self.close_page()

    
    async def parse_page(self):
        # parse self.currPage
        page = self.currPage
        return None
    
    def send_to_processing(self, result):
        return None
        

    async def click(self, css):
        await self.currPage.click(css)


    def _convert_CT_url(self, CT):
        # convert CT dict to url
        return self.template_url.format(C1 = CT["C1"], C2 = CT["C2"], T = CT["T"])
    
    def _convert_to_datetime(self, strDate):
        return datetime.datetime.strptime(strDate, '%Y-%m-%d')

    def _convert_url_CT(self, url):
        # convert url to CT dict
        parsed = parse.parse(self.template_url, url)

        if not parsed is None:
            return parsed.named
        else:
            return None

    def _need_goto_page(self, CT):
        if self.currCT is None:
            return True
        
        same_C = self.currCT["C1"] == CT["C1"] and self.currCT["C2"] == CT["C2"]
        close_T = abs(self._convert_to_datetime(self.currCT["T"]) - \
                      self._convert_to_datetime(CT["T"])) <= 3
        
        return same_C and close_T
        
    

connect = pyppeteer_connection()
asyncio.get_event_loop().run_until_complete(connect.check_tickets({"C1": "BJS", "C2": "SHA", "T": "2021-07-12"}))
