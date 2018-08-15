from bs4 import BeautifulSoup
import requests
import json
import datetime
from lxml import etree, html

class PerformanceStats:

    YAHOO_FINANCE_SPAN_TAG_CLASS_NAME = "Bdbw(1px) Bdbc($screenerBorderGray) Bdbs(s) H(25px) Pt(10px)"


    def get_performance_stats(self, fund_symbol):
        """
        Grabs performance stats. Grabs 3 things:
            1. Data for the Growth of $10,000
            2. Trailing returns for the time periods (1 month, 3 month, 6 month, YTD, 1 year, 3 year, 5 year, 10 year, 15 year)
            3. Historical annual total returns for each year (current year until earliest date)
        Return in a JsonResponse encoded object
        """
        print("")

    def get_10000_growth(self, fund_symbol):
        print("")

    def get_trailing_returns(self, fund_symbol):
        """
        Grabs trailing returns for the time periods (1 month, 3 month, 6 month, YTD, 1 year, 3 year, 5 year, 10 year, 15 year)
        Source = Morningstar
        Input:      Fund symbol, 5 letter acronym, string
        Returns:    Dict with return values, key = time period, value = return
        """
        # Build a dictionary, where key = time period, value = trailing return for that time period.
        timespans = ["1-Month", "3-Month", "6-Month", "YTD",
                     "1-Year", "3-Year", "5-Year", "10-Year", "15-Year"]
        dictionary = {}
        url = self.build_performance_url(fund_symbol)
        try:
            raw = requests.get(url)
            if raw != None:
                soup = BeautifulSoup(raw.text, 'html.parser')

                # Find corresponding column values of trailing returns. These will be the values of the dict
                table = soup.find("table")
                rows = table.findAll(lambda tag: tag.name == 'tr')
                for row in rows:
                    row_header = row.find("th")
                    if row_header.text == fund_symbol:
                        quarterly_returns = [col.text for col in row.findAll("td")]
                        dictionary = dict(zip(timespans, quarterly_returns))
        except Exception as e: # Not good to have a catch-all exception, but I'll create custom exceptions later
            print e

        return dictionary


    def build_performance_url(self, fund_symbol):
        return "http://performance.morningstar.com/perform/Performance/fund/trailing-total-returns.action?&t=" + fund_symbol + "&cur=&ops=clear&s=0P00001L8R&ndec=2&ep=true&align=q&annlz=true&comparisonRemove=false&loccat=&taxadj=&benchmarkSecId=&benchmarktype="

    def get_fund_historical_returns(self, fund_symbol):
        """
        Grabs historical annual total returns for each year (current year until earliest date), for both the fund, and its category
        Source = Yahoo Finance
        Input:      Fund symbol, 5 letter acronym, string
        Returns:    Dict that contains 2 dicts. Each dict has key=year, value=return
        """
        url = self.build_historical_url(fund_symbol)
        raw = requests.get(url)
        if raw != None:
            historical_returns = self.scrape_historical_returns(fund_symbol, url)
            if historical_returns != None:
                return historical_returns

    def build_historical_url(self, fund_symbol):
        return "https://finance.yahoo.com/quote/" + fund_symbol + "/performance?p=" + fund_symbol

    def scrape_historical_returns(self, fund_symbol, url):
        columns = self.extract_raw_column_data(fund_symbol, url)
        return self.build_json_response(columns, fund_symbol)

    def extract_raw_column_data(self, fund_symbol, url):
        """
        Extracts column data as Element objects from url

        https://stackoverflow.com/questions/14299978/how-to-use-lxml-to-find-an-element-by-text

        Process:
            Given this html from https://finance.yahoo.com/quote/PRHSX/performance?p=PRHSX:
            <div class="Mb(25px) " data-reactid="121">
                 <h3 data-reactid="122">
                    <span data-reactid="123">Annual Total Return (%) History</span>     <--Start here
                </h3>
                 <div data-reactid="124">
                    <div class="Bdbw(1px) Bdbc($screenerBorderGray) Bdbs(s) H(20px) Pt(10px) C($c-fuji-grey-j) Fz(xs) Fw(400)" data-reactid="125">some irrelevant stuff here</div>
                    <div class="Bdbw(1px) Bdbc($screenerBorderGray) Bdbs(s) H(25px) Pt(10px)" data-reactid="134"> Data column for 2018 with 4 spans that we want to extract </div>
                    <div class="Bdbw(1px) Bdbc($screenerBorderGray) Bdbs(s) H(25px) Pt(10px)" data-reactid="134"> Data column for 2017 with 4 spans that we want to extract </div>
                    ....
                    <div class="Bdbw(1px) Bdbc($screenerBorderGray) Bdbs(s) H(25px) Pt(10px)" data-reactid="134"> Data column for 1996 with 4 spans that we want to extract </div>

            1. Find the span tag that has text "Annual Total Return (%) History". This our starting point
            2. Navigate up to its parent tag, then go to sibiling tag that has the data we actually need, then grab that data
        """

        #Build lxml tree from webpage
        page = requests.get(url)
        tree = html.fromstring(page.content)

        #Find the H3 tag that says Annual Total Return (%) History
        h3_span_text = tree.xpath('.//span[text()="Annual Total Return (%) History"]')

        #The table we wnat is in a div tag, which is a sibling to h3. The h3 and the div tag are under one overarching div tag. Get h3's sibiling
        h3 = h3_span_text[0].getparent()
        table = h3.getnext()

        #Grab all columns as lxml Element objects that have the historical return data in them, aka if the div tag looks like this: <div class="Bdbw(1px) Bdbc($screenerBorderGray) Bdbs(s) H(25px) Pt(10px)" data-reactid="148"></div>
        viable_columns_as_elements = []
        for column in list(table):
            class_item = [item for item in column.items() if "class" in item and YAHOO_FINANCE_SPAN_TAG_CLASS_NAME in item]
            if len(class_item) == 1:
                viable_columns_as_elements.append(column)

        return viable_columns_as_elements

    def build_json_response(self, column_data, fund_symbol):
        """
        Take the extracted column data and put it into a JSON response format for all data except current year.
        Converts list of column data as Element objects --> 2 dicts in the following format:
        {
            fund_symbol: {
                "2017": 27.95,
                ...
                "1996": 26.75
            },
            category: {
                "2017": 24.31,
                ...
                "1996": 13.5
            }
        }
        """

        current_year = str(datetime.datetime.now().year)
        fund = {}
        category = {}
        response = {}

        for col in column_data:
            data = [str(span.text_content()) for span in list(col)]
            if current_year not in data and len(data) == 4:    #Grab column data for all years except current year
                #Data will be in the format of a list of 4 elements, in the order [year, ui bar, fund return, category return]. We hardcode order, as Elements are returned in document order, according to documentation
                year = int(data[0])
                fund_return = float(data[2][:-1])           #Concatenate "%" off of string, then convert to float. Ex: "25.67%", we want: 25.67
                category_return = float(data[3][:-1])       #Concatenate "%" off of string, then convert to float. Ex: "25.67%", we want: 25.67
                fund[year] = fund_return
                category[year] = category_return

        response[fund_symbol] = fund
        response["Category"] = category
        return response



p = PerformanceStats()
print(p.get_trailing_returns("PRHSX"))
print(p.get_fund_historical_returns("PRHSX"))
