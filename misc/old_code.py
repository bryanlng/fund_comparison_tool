from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import json
from lxml import etree, html
import urllib2
from lxml.html.soupparser import fromstring
from lxml.etree import tostring
from io import StringIO, BytesIO
import datetime


"""
Old selenium code for historical returns. Worked, but took 5 seconds to do it. Replaced with lxml implementation
"""
# def scrape_historical_returns(self, fund_symbol, url):
#         raw_values = self.extract_values(fund_symbol, url)
#         values = self.remove_unnecessary_values(raw_values, fund_symbol)
#         return self.build_json_response(values, fund_symbol)

# def extract_values(self, fund_symbol, url):
#     """
#     Selenium remote webdriver WebElement attributes and methods
#     https://seleniumhq.github.io/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webelement.html
#     http://elementalselenium.com/tips/38-headless
#     https://stackoverflow.com/questions/6183276/how-do-i-run-selenium-in-xvfb
#     """

#     #Initialize selenium in Chrome
#     # display = Display(visible=0, size=(800, 600))
#     # display.start()
#     vdisplay = Xvfb()
#     vdisplay.start()
#     driver = webdriver.Chrome("/u/bryanlng/scrape/chromedriver_linux")     #utcs machines location
#     driver.get(url)

#     #Extract values using find_element_by_xpath.
#     #For reference, we are scraping the data table under the performance page for a mutual fund on Yahoo Finance's "Annual Total Return (%) History"
#     parent = driver.find_element_by_xpath("""//*[@id="Col1-0-Performance-Proxy"]/section/div[3]/h3/span""")
#     historicals = parent.find_elements_by_xpath("""//*[@id="Col1-0-Performance-Proxy"]/section/div[3]/div""")
#     raw_text = str(historicals[0].text)
#     # driver.quit()
#     # display.stop()
#     driver.quit()
#     vdisplay.stop()
#     return raw_text.split("\n")

# def remove_unnecessary_values(self, values, fund_symbol):
#     """
#     Remove unnecessary values such as ["Year", fund name, "Category", current year, "N/A"]
#     Need to remove current year + n/a, as the return for the current year is "N/A"
#     """
#     now = datetime.datetime.now()
#     to_remove = ["Year", fund_symbol, "Category", str(now.year), "N/A"]
#     return [v for v in values if v not in to_remove]

# def build_json_response(self, values, fund_symbol):
#     """
#     Precondition: List length must be a multiple of 3, or else it'll break and we'll get IndexError
#     Assuming 2018 is current year, don't include 2018, start at 2017, as 2018 is "N/A"
#     Converts list of string values --> 2 dicts in the following format:
#     {
#         fund_symbol: {
#             "2017": 27.95,
#             ...
#             "1996": 26.75
#         },
#         category: {
#             "2017": 24.31,
#             ...
#             "1996": 13.5
#         }
#     }
#     """
#     response = {}
#     fund = {}
#     category = {}
#     for i in range(0,len(values),3):
#         fund_return = values[i+1]
#         category_return = values[i+2]
#         fund[values[i]] = float(fund_return[:-1])
#         category[values[i]] = float(category_return[:-1])

#     response["fund_symbol"] = fund
#     response["category"] = category
#     return response