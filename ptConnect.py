import pandas as pd
from pyppeteer import launch
from pyquery import PyQuery as pq
import datetime
import asyncio
import parse
import pyppeteer

from ConnectParent import Connector
from TaskManager import TaskManager
from Task import Task

from ErrorCode import ErrorCode


class pyppeteer_connection(Connector):
    # each connection corresponds to a proxy ip
    # each ip would survive for couple searches
    # proxy format: 123.123.123.123:1234

    # this class would be instantiate in a normal for loop
    # then send to asyncio event to run the main loop
    # within the loop:
    #   1. retrieve task from TaskManager
    #   2. goto the page
    #   3. parse the page
    #   4. send the parsed page to the next processing step
    #   5. report task back to TaskManager
    #   6. close page
    #   7. repeat 1-5 until proxy is dead
    #   8. close browser
    # if the proxy is dead, the browser would be closed, and the instance would be killed

    def __init__(self, proxy):
        self.proxy = proxy

        self.url_mainPage = "https://ctrip.com"
        self.template_url = 'https://flights.ctrip.com/international/search/oneway-{C1}-{C2}?depdate={T}'

        self.pages = []
        self.CTs = []

        self.currPage = None
        self.currCT = None

        self.browser = None

        Connector.__init__(self)

    async def main(self, tasks):
        await self.create_browser()

        while not tasks.allCompleted():  # condition here is incorrect

            #   1. retrieve task from TaskManager
            task = tasks.getTask()

            #   2. goto the page
            CT = task.getCT()
            try:
                await self.new_page(self._convert_CT_url(CT))
            except pyppeteer.errors.TimeoutError:
                task.markError(ErrorCode.get("pyppeteer.errors.TimeoutError"))
                tasks.reportTask(task)
                await self.close_page()
                continue
            except pyppeteer.errors.PageError:
                task.markError(ErrorCode.get("pyppeteer.errors.PageError"))
                tasks.reportTask(task)
                await self.close_page()
                continue

            await asyncio.sleep(10)

            # scroll to the bottom
            # await self.currPage.evaluate('window.scrollBy(0, document.body.scrollHeight)')
            for _ in range(6):
                await self.currPage.evaluate('_ => {window.scrollBy(0, window.innerHeight/1.5);}')
            # await self.currPage.hover(".footer-wrapper")
                await asyncio.sleep(1)

            #   3. parse the page
            try:
                result = await self.parse_page()
            except ValueError:
                task.markError(ErrorCode.get("page content length too small"))
                tasks.reportTask(task)
                await self.close_page()
                continue

            #   4. send the parsed page to the next processing step
            self.send_to_processing(result)

            #   5. report task back to TaskManager
            task.markCompleted()
            tasks.reportTask(task)

            print("Page completed")

            #   6. close page
            await self.close_page()

        #   8. close browser
        await self.close_browser()

    async def create_browser(self):
        self.browser = await launch(headless=False, devtools=True, args=['--disable-infobars', '--proxy-server={}'.format(self.proxy),
                                                                         '--window-size=1792,1120'], dumpio=False)

    async def close_browser(self):
        await self.browser.close()

    async def new_page(self, url=None, goto_or_not=True):
        # go to page with url
        # when url is None: go to a new empty page
        # sometimes the target CT is close to current CT,
        # so a simple click would be better

        if url is None:
            self.currPage = await self.browser.newPage()
            self.pages.append(self.currPage)
            self.currCT = None
            self.CTs.append(None)

        if goto_or_not is True:
            tempPage = await self.browser.newPage()

            await tempPage.setViewport({'width': 1792, 'height': 1120})

            await tempPage.setUserAgent(self._choose_user_agent())

            await tempPage.evaluateOnNewDocument(
                '() =>{ Object.defineProperties(navigator, { webdriver:{ get: () => false } }) }')

            await tempPage.goto(url, {'waitUntil': 'load', 'timeout': 1000*10})

            self.pages.append(tempPage)
            self.currPage = tempPage
            self.currCT = self._convert_url_CT(url)
            self.CTs.append(self.currCT)

        else:
            # click on the page
            # not completed yet
            # might be unnecessary
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
            # if only one page exists in the browser
            assert len(self.CTs) == 1
            self.currPage = None
            self.pages.pop()
            self.currCT = None
            self.CTs.pop()
        else:
            # multiple pages exist
            self.pages.pop()
            self.currPage = self.pages[-1]
            self.CTs.pop()
            self.currCT = self.CTs[-1]
            assert len(self.currPage) == len(self.CTs)

    # !!! not usable now
    # rewriting
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
        # parse self.currPage, which should be the data page of a flight search
        # only the first 15 flights are recorded
        result = []

        content = await self.currPage.content()
        print(len(content))
        if len(content) < 200000:
            raise ValueError

        doc = pq(content)
        flights = doc('.flight-list .flight-box').items()
        for flight in flights:
            r = {'FlightNumber': flight('.flight-airline .plane-No').text().split('\xa0')[0],
                 'Airplane': flight('.flight-airline .plane-No span').text(),
                 'Airline': flight('.flight-airline .airline-name').text(),
                 'deptTime': flight('.flight-detail .depart-box .time').text(),
                 'deptAirport': flight('.flight-detail .depart-box .airport span').text().rstrip(' '),
                 'arrTime': flight('.flight-detail .arrive-box .time').text(),  # might be "00:45+1天"
                 'arrAirport': flight('.flight-detail .arrive-box .airport span').text().rstrip(' '),
                 'Price': flight('.flight-price span.price').text().strip('¥')}  # info of this flight
            result.append(r)

        return result

    def send_to_processing(self, result):
        # send to the next step
        # flightInformation.flightInfo.extend(result)
        return None

    async def click(self, css):
        # helper func
        await self.currPage.click(css)

    # private methods

    def _convert_CT_url(self, CT):
        # convert CT dict to url
        return self.template_url.format(C1=CT.get("C1"), C2=CT.get("C2"), T=CT.get("T"))

    @staticmethod
    def _convert_to_datetime(strDate):
        return datetime.datetime.strptime(strDate, '%Y-%m-%d')

    def _convert_url_CT(self, url):
        # convert url to CT dict
        parsed = parse.parse(self.template_url, url)  # anti str.format

        if parsed is not None:
            return parsed.named
        else:
            return None

    def _need_goto_page(self, CT):
        # determines if a click can replace goto new page
        """
        if self.currCT is None:
            return True

        same_C = self.currCT["C1"] == CT["C1"] and self.currCT["C2"] == CT["C2"]
        close_T = abs(self._convert_to_datetime(self.currCT["T"]) -
                      self._convert_to_datetime(CT["T"])) <= 3

        return same_C and close_T
        """
        return True  # goto page all the time, not clicking

'''
# global object TaskManager
tasks = TaskManager([Task('BJS', 'SHA', '2021-08-12'),
                     Task('SHA', 'BJS', '2021-08-24'),
                     #Task('CKG', 'BJS', '2021-08-13'),
                     #Task('SHA', 'CKG', '2021-08-31'),
                     Task('BJS', 'CKG', '2021-08-01'),
                     #Task('SYX', 'BJS', '2021-08-14'),
                     # Task('SYX', 'SHA', '2021-08-18'),
                     Task('CKG', 'SYX', '2021-08-19')])


# tasks = TaskManager([Task('BJS', 'SHA', '2021-08-12')])

class Result:
    def __init__(self):
        self.flightInfo = []


flightInformation = Result()

connect = pyppeteer_connection('60.173.24.231:49337')
asyncio.get_event_loop().run_until_complete(connect.main())

df = pd.DataFrame(flightInformation.flightInfo)
df.to_csv('/Users/Hanbo/Desktop/result.csv')
'''
