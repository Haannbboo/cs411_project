import asyncio
import pandas as pd

from Task import Task
from ptConnect import pyppeteer_connection
# from TaskGenerator import Generator
from TaskManager import TaskManager


# Main function for data collection
# Given C1 C2 T, first generate tasks, then ptConnect collects all data

class Result:
    def __init__(self):
        self.flightInfo = []


tasks = TaskManager([Task('BJS', 'SHA', '2021-08-12')])

flightInformation = Result()
connect = pyppeteer_connection('60.173.24.231:49337')
asyncio.get_event_loop().run_until_complete(connect.main(tasks))

# df = pd.DataFrame(flightInformation.flightInfo)
# df.to_csv('/Users/Hanbo/Desktop/result.csv')


# 1. Collect
