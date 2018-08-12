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

"""
https://stackoverflow.com/questions/17196018/extracting-table-contents-from-html-with-python-and-beautifulsoup
http://performance.morningstar.com/perform/Performance/fund/trailing-total-returns.action?&t=XNAS:PRHSX&region=usa&culture=en-US&cur=&ops=clear&s=0P00001L8R&ndec=2&ep=true&align=q&annlz=true&comparisonRemove=false&loccat=&taxadj=&benchmarkSecId=&benchmarktype=

difference between daily, monthly, quarterly, is in align field. For quarterly, align="q"
https://stackoverflow.com/questions/209840/convert-two-lists-into-a-dictionary-in-python
"""

# url = "http://performance.morningstar.com/perform/Performance/fund/trailing-total-returns.action?&t=XNAS:PRHSX&region=usa&culture=en-US&cur=&ops=clear&s=0P00001L8R&ndec=2&ep=true&align=q&annlz=true&comparisonRemove=false&loccat=&taxadj=&benchmarkSecId=&benchmarktype="
# raw = requests.get(url)
# text = raw.text
# soup = BeautifulSoup(text, 'html.parser')
# table = soup.find("table")
# rows = table.findAll(lambda tag: tag.name == 'tr')
# dictionary = {}  # Dictionary: key = time period, value = trailing return for that time period. Ex: {u'3-Month': u'6.31', u'1-Month': u'1.57', u'3-Year': u'5.11', u'10-Year': u'17.19', u'15-Year': u'15.35', u'6-Month': u'7.75', u'YTD': u'7.75', u'1-Year': u'15.32', u'5-Year': u'18.52'}

# # Find time span values of trailing returns. These will be the keys of the dict
# th_timespans = rows[0].findAll("th")
# timespans = [
#     timespan.text for timespan in th_timespans if "Total Return " not in timespan.text]
# # print(timespans)

# # Find corresponding column values of trailing returns. These will be the values of the dict
# for row in rows:
#     # print row
#     row_header = row.find("th")
#     if row_header.text == "PRHSX":
#         # print row_header.text
#         cols = row.findAll("td")
#         column_values = [col.text for col in cols]

#         # Create dictionary from timespans and column_values
#         dictionary = dict(zip(timespans, column_values))
#         print(dictionary)
    # print row
    # print ("")
# print(type(rows))
# print(rows)


###Selenium stuff, using pyvirtualdisplay

###Selenium stuff, using headless chrome
# webdriver =
# options = webdriver.ChromeOptions()
# options.add_experimental_option("excludeSwitches",["ignore-certificate-errors"])
# options.add_argument('--disable-gpu')
# options.add_argument('--headless')


#lxml stuff
"""
https://stackoverflow.com/questions/11465555/can-we-use-xpath-with-beautifulsoup
"""

def build_historical_url(fund_symbol):
        return "https://finance.yahoo.com/quote/" + fund_symbol + "/performance?p=" + fund_symbol

# fund_symbol = "PRHSX"
# url =  build_historical_url(fund_symbol)
# response = urllib2.urlopen(url)
# htmlparser = etree.HTMLParser()
# tree = etree.parse(response, htmlparser)
# xpath = etree.XPath("""//*[@id="Col1-0-Performance-Proxy"]/section/div[3]/div""")
# print(xpath)
# text = xpath()


"""
https://stackoverflow.com/questions/33711514/why-lxml-isnt-finding-xpath-given-by-chrome-inspector
https://stackoverflow.com/questions/23900348/why-does-this-xpath-fail-using-lxml-in-python
"""

# fund_symbol = "PRHSX"
# url =  build_historical_url(fund_symbol)
# page = requests.get(url)
# tree = html.fromstring(page.content)
# print(tree)

"""
https://lxml.de/elementsoup.html
"""
# fund_symbol = "PRHSX"
# url =  build_historical_url(fund_symbol)
# raw = requests.get(url)
# tag_soup = raw.text.encode('utf-8').strip()
# root = fromstring(tag_soup)
# span = fromstring(tag_soup).find('div')
# print(span)

"""
https://lxml.de/parsing.html#parsing-html
https://lxml.de/lxmlhtml.html
"""
fund_symbol = "PRHSX"
url =  build_historical_url(fund_symbol)
raw = requests.get(url)
broken_html = raw.text
parser = etree.HTMLParser()
tree   = etree.parse(StringIO(broken_html), parser)
result = etree.tostring(tree.getroot(),  pretty_print=True, method="html")
print(result)
