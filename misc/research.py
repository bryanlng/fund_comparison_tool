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


##########################################################################################################################################################################
###################################################################################lxml research##########################################################################
##########################################################################################################################################################################

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
# fund_symbol = "PRHSX"
# url =  build_historical_url(fund_symbol)
# raw = requests.get(url)
# broken_html = raw.text
# parser = etree.HTMLParser()
# tree   = etree.parse(StringIO(broken_html), parser)
# result = etree.tostring(tree.getroot(),  pretty_print=True, method="html")
# print(result)


"""
https://docs.python-guide.org/scenarios/scrape/
https://lxml.de/lxmlhtml.html#parsing-html
HTML elements have all the methods that come with ElementTree, but also include some extra methods:

Methods:
https://lxml.de/api/lxml.html.HtmlElement-class.html
addnext', 'addprevious', 'append', 'attrib', 'base', 'base_url', 'body', 'classes', 'clear', 'cssselect', 'drop_tag', 'drop_tree', 
'extend', 'find', 'find_class', 'find_rel_links', 'findall', 'findtext', 'forms', 'get', 'get_element_by_id', 'getchildren', 'getiterator', 
'getnext', 'getparent', 'getprevious', 'getroottree', 'head', 'index', 'insert', 'items', 'iter', 'iterancestors', 'iterchildren', 
'iterdescendants', 'iterfind', 'iterlinks', 'itersiblings', 'itertext', 'keys', 'label', 'make_links_absolute', 'makeelement', 'nsmap', 
'prefix', 'remove', 'replace', 'resolve_base_href', 'rewrite_links', 'set', 'sourceline', 'tag', 'tail', 'text', 'text_content', 'values', 'xpath'

Pertinent methods:
1. items(self):
    -gets element attributes, as a sequence. The attributes are returned in an arbitrary order.

2. getchildren(self):
    -returns all direct children, as HtmlElement objects   , <class 'lxml.html.HtmlElement'>
    -Avoid using this, as this has been DEPRECATED. New code should use list(element) or simply iterate over elements. 
    -https://lxml.de/api/lxml.etree._Element-class.html#getchildren


Bdbw(1px) Bdbc($screenerBorderGray) Bdbs(s) H(25px) Pt(10px)
"""
fund_symbol = "PRHSX"
url =  build_historical_url(fund_symbol)
page = requests.get(url)
tree = html.fromstring(page.content)
# print(tree)     #HtmlElement object, <class 'lxml.html.HtmlElement'>
# print(type(tree))   
# print(dir(tree))
# print(tree.text_content())
# print(tree.xpath())
# print(tree.items())
# children = tree.getchildren()
# for c in children:
#     print(type(c))
# buyers = tree.xpath('//html/body/div[1]/div/div[1]/div[1]/div/div[3]/div[1]/div/div[1]/div/div/section/div[3]/div[@class="Bdbw(1px) Bdbc($screenerBorderGray) Bdbs(s) H(25px) Pt(10px)"]/text()')
# print(buyers)

"""
https://stackoverflow.com/questions/14299978/how-to-use-lxml-to-find-an-element-by-text
"""

#Find the H3 tag that says Annual Total Return (%) History
e = tree.xpath('.//span[text()="Annual Total Return (%) History"]')

#The table we wnat is in a div tag, which is a sibling to h3. The h3 and the div tag are under one overarching div tag. Get h3's sibiling
h3 = e[0].getparent()
print(h3)
table = h3.getnext()

#Grab all columns as Element objects that have the historical return data in them. In the case of PRHSX, it should be this year (2018) to its starting date (1996). There should be 23 elements
viable_columns_as_elements = []
for column in list(table):
    class_item = [item for item in column.items() if "class" in item and "Bdbw(1px) Bdbc($screenerBorderGray) Bdbs(s) H(25px) Pt(10px)" in item]
    if len(class_item) == 1:
        viable_columns_as_elements.append(column)

#Extract data out of viable columns. Extract all data except for data this year. Each column is a div tag that contains 4 span columns for year, ui bar, fund return, category return. We only want year, fund return, category return.
current_year = str(datetime.datetime.now().year)
fund = {}
category = {}
response = {}
for col in viable_columns_as_elements:
    data = [str(span.text_content()) for span in list(col)]
    if current_year not in data:
        #Data will be in the format of a list of 4 elements, in the order [year, ui bar, fund return, category return]. We hardcode order, as Elements are returned in document order, according to documentation
        year = int(data[0])
        fund_return = float(data[2][:-1])
        category_return = float(data[3][:-1])
        fund[year] = fund_return
        category[year] = category_return

response[fund_symbol] = fund
response["category"] = category
print(fund)
print(category)


#Trying to iterate div's children using iterchildren(), before I found an easier way to do it using list(elem)

# for c in enclosing_div_children:
#     print(c.tag)
# print(k)
# enclosing_div_iterator = enclosing_div.iterchildren()   #<lxml.etree.ElementChildIterator object at 0x7f6641461140>
# table = None
# while True:
#     try:
#         elem = enclosing_div_iterator.next()
#         if elem.tag == "div":
#             table = elem
#             print(elem.tag)
#     except StopIteration:
#         break


# table_iterator = table.iterchildren()   #<lxml.etree.ElementChildIterator object at 0x7f6641461140>
# viable_columns_as_elements = []
# while True:
#     try:
#         column = table_iterator.next()
#         items = column.items()
#         print("new column")
#         print(column)
#         print("items: ", items)
#         class_item = [item for item in items if "class" in item and "Bdbw(1px) Bdbc($screenerBorderGray) Bdbs(s) H(25px) Pt(10px)" in item]
#         if len(class_item) == 1:
#             viable_columns_as_elements.append(column)
#     except StopIteration:
#         break

# for element in viable_columns_as_elements:
