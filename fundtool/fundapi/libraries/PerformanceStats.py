from bs4 import BeautifulSoup
from lxml import etree, html
from enum import Enum
import requests
import json
import datetime
import ast
import re

import fundtool.fundapi.libraries.PerformanceStats as FundException

class Section(Enum):
    TRAILING = "trailing_returns"
    GROWTH = "10000_growth"
    HISTORICAL = "historical"

class PerformanceStats:

    def get_performance_stats(self, fund_symbol):
        fund_symbol = fund_symbol.upper()
        stats = {}
        stats["trailing_returns"] = self.get_trailing_returns(fund_symbol)
        stats["historical_returns"] = self.get_fund_historical_returns(fund_symbol)
        stats["10000_growth_data"] = self.get_10000_growth(fund_symbol)
        return stats

    def get_10000_growth(self, fund_symbol):
        response = {}
        url = self.build_url(Section.GROWTH, fund_symbol)
        raw_data = requests.get(url)
        if raw_data.status_code == 200:
            raw_json = raw_data.json();
            html = raw_json["html"]

            #Interpret HTML using BeautifulSoup, then extract out data in JSON from <div data_mod_config = ...., class = mod-ui-chart--dynamic>
            soup = BeautifulSoup(html, 'html.parser')
            response = {}
            try:
                data_mod_config_div = soup.find("div", {"class": "mod-ui-chart--dynamic"})["data-mod-config"]
                growth_json = ast.literal_eval(data_mod_config_div)
                internal_data = growth_json["data"]
                if len(internal_data) >= 1:

                    #Access first element in the dict, which is the list of values
                    growths = next(iter(internal_data.values()))

                    #Parse into a dict where key = date (YYYY-MM-DD, removing the "T00:00:00" from the end), value = expected dollar value that year
                    response = {year["date"][:len(year["date"])-9] : year["value"] for year in growths}
            except Exception as e:
                raise FundException.UIChangedError(f"UI changed for symbol name: {fund_symbol}; thus, we cannot scrape")

            return response
        else:
            raise FundException.SymbolDoesNotExistError(f"Invalid symbol name: {fund_symbol}")


    def get_trailing_returns(self, fund_symbol):
        # Build a dictionary, where key = time period, value = trailing return for that time period.
        timespans = ["1-Month", "3-Month", "6-Month", "YTD",
                     "1-Year", "3-Year", "5-Year", "10-Year", "15-Year"]
        response = {}
        url = self.build_url(Section.TRAILING, fund_symbol)
        try:
            raw = requests.get(url)
            if raw.status_code == 200:
                soup = BeautifulSoup(raw.text, 'html.parser')

                # Find corresponding column values of trailing returns. These will be the values of the dict
                table = soup.find("table")
                rows = table.findAll(lambda tag: tag.name == 'tr')
                for row in rows:
                    row_header = row.find("th")
                    if row_header.text == fund_symbol:
                        quarterly_returns = [col.text for col in row.findAll("td")]
                        response = dict(zip(timespans, quarterly_returns))
        except Exception as e: # Not good to have a catch-all exception, but I'll create custom exceptions later
            print(e)

        return response


    def get_fund_historical_returns(self, fund_symbol):
        url = self.build_url(Section.HISTORICAL, fund_symbol)
        raw = requests.get(url)
        if raw != None:
            historical_returns = self.scrape_historical_returns(fund_symbol, url)
            if historical_returns != None:
                return historical_returns

    def scrape_historical_returns(self, fund_symbol, url):
        columns = self.extract_raw_column_data(fund_symbol, url)
        return self.build_json_response(columns, fund_symbol)

    def extract_raw_column_data(self, fund_symbol, url):
        #Build lxml tree from webpage
        page = requests.get(url)
        tree = html.fromstring(page.content)

        #Find the H3 tag that says Annual Total Return (%) History
        h3_span_text = tree.xpath('.//span[text()="Annual Total Return (%) History"]')

        #The table we wnat is in a div tag, which is a sibling to h3. The h3 and the div tag are under one overarching div tag. Get h3's sibiling
        h3 = h3_span_text[0].getparent()
        table = h3.getnext()

        #Grab all columns as lxml Element objects. This includes the 2 columns we don't want (placeholder value column + current year), so we need to filter them out.
        columns = [column for column in list(table)]

        #Assuming elements are in document order, we can just remove the first 2 elements of the list
        del columns[0:2]

        #Return filtered version
        return columns

    def build_json_response(self, column_data, fund_symbol):
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

    def build_url(self, section, fund_symbol):
        if section == Section.TRAILING:
            return "http://performance.morningstar.com/perform/Performance/fund/trailing-total-returns.action?&t=" + fund_symbol + "&cur=&ops=clear&s=0P00001L8R&ndec=2&ep=true&align=q&annlz=true&comparisonRemove=false&loccat=&taxadj=&benchmarkSecId=&benchmarktype="
        elif section == Section.GROWTH:
            return "https://markets.ft.com/data/funds/ajax/US/get-comparison-panel?data={\"comparisons\":[\"" + fund_symbol + "\"],\"openPanels\":[\"Performance\"]}"
        else:
            return "https://finance.yahoo.com/quote/" + fund_symbol + "/performance?p=" + fund_symbol

    def hasGoodSyntax(self, fund_symbol):
        return len(fund_symbol) == 5 and re.match('^[\A-Z-]{5}$', k) is not None


p = PerformanceStats()
fund_symbol = "PRHSX"
print(p.get_10000_growth(fund_symbol))
# print(p.get_trailing_returns(fund_symbol))
# print(p.get_fund_historical_returns(fund_symbol))
# print(p.get_performance_stats(fund_symbol))
