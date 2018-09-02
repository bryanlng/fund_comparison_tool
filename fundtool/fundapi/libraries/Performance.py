from bs4 import BeautifulSoup
from lxml import etree, html
import requests
import json
import datetime
import ast
import sys

import fundapi.libraries.util as Util
from fundapi.libraries.util import Section
import fundapi.libraries.exceptions as FundException

class PerformanceStats:
    def get_performance_stats(self, fund_symbol):
        stats = {}
        try:
            Util.validateFormat(fund_symbol)
            stats["trailing_returns"] = self.get_trailing_returns(fund_symbol)
            stats["historical_returns"] = self.get_fund_historical_returns(fund_symbol)
            stats["10000_growth_data"] = self.get_10000_growth(fund_symbol)

        except FundException.ImproperSymbolFormatError as e:
            raise FundException.ImproperSymbolFormatError(e)
        except FundException.SymbolDoesNotExistError as e:
            raise FundException.SymbolDoesNotExistError(e)
        except FundException.UIChangedError as e:
            raise FundException.UIChangedError(e)
        except FundException.SourceEndpointChangedError as e:
            raise FundException.SourceEndpointChangedError(e)

        return stats


    def get_10000_growth(self, fund_symbol):
        response = {}
        url = Util.build_url(Section.GROWTH, fund_symbol)
        raw = requests.get(url)

        if raw.status_code == 200 and raw.text != "":
            raw_json = {}
            try:
                raw_json = raw.json();
            except Exception as e:
                raise FundException.SymbolDoesNotExistError(f"Error while retrieving data for $10000 growth: Symbol does not exist: {fund_symbol}")

            #Interpret HTML using BeautifulSoup, then extract out data in JSON from <div data_mod_config = ...., class = mod-ui-chart--dynamic>
            html = raw_json["html"]
            soup = BeautifulSoup(html, 'html.parser')
            response = {}
            data_mod_config_div = soup.find("div", {"class": "mod-ui-chart--dynamic"})["data-mod-config"]
            if data_mod_config_div != "":
                #Convert dictionary in string form to an actual dictionary
                growth_json = ast.literal_eval(data_mod_config_div)
                internal_data = growth_json["data"]
                if len(internal_data) >= 1:
                    #Access first element in the dict, which is the list of values
                    growths = next(iter(internal_data.values()))

                    #Parse into a dict where key = date (YYYY-MM-DD, removing the "T00:00:00" from the end), value = expected dollar value that year
                    response = {year["date"][:len(year["date"])-9] : year["value"] for year in growths}
            else:
                raise FundException.UIChangedError(f"Error while retrieving data for $10000 growth: UI changed for symbol name: {fund_symbol}; thus, we cannot scrape")
        else:
            raise FundException.SymbolDoesNotExistError(f"Error while retrieving data for $10000 growth: Symbol does not exist: {fund_symbol}")

        return response


    def get_trailing_returns(self, fund_symbol):
        # Build a dictionary, where key = time period, value = trailing return for that time period.
        timespans = ["1-Month", "3-Month", "6-Month", "YTD",
                     "1-Year", "3-Year", "5-Year", "10-Year", "15-Year"]
        response = {}
        url = Util.build_url(Section.TRAILING, fund_symbol)
        raw = requests.get(url)
        if raw.status_code == 200 and raw.text != "":
            soup = BeautifulSoup(raw.text, 'html.parser')

            # Find corresponding column values of trailing returns. These will be the values of the dict
            table = soup.find("table")

            if table is not None:
                rows = table.findAll(lambda tag: tag.name == 'tr')
                for row in rows:
                    row_header = row.find("th")
                    if row_header.text == fund_symbol:
                        quarterly_returns = [col.text for col in row.findAll("td")]
                        response = dict(zip(timespans, quarterly_returns))
            else:
                raise FundException.UIChangedError(f"Error while retrieving data for trailing returns: UI for source website of this symbol has changed, so we can't scrape the data: {fund_symbol}")
        else:
            raise FundException.SymbolDoesNotExistError(f"Error while retrieving data for trailing returns: Symbol does not exist: {fund_symbol}")

        return response


    def get_fund_historical_returns(self, fund_symbol):
        url = Util.build_url(Section.HISTORICAL, fund_symbol)
        raw = requests.get(url)
        if raw.status_code == 200 and raw.text != "":
            return self.retrieve_historical_returns(fund_symbol, url, raw)
        else:
            raise FundException.SymbolDoesNotExistError(f"Error while retrieving data for historical returns: Symbol does not exist: {fund_symbol}")

    def retrieve_historical_returns(self, fund_symbol, url, page):
        columns = self.scrape_historical_column_data(fund_symbol, url, page)
        return self.build_historical_return_response(columns, fund_symbol)

    def scrape_historical_column_data(self, fund_symbol, url, page):
        #Build lxml tree from webpage
        tree = html.fromstring(page.content)

        #Find the H3 tag that says Annual Total Return (%) History
        h3_span_text = tree.xpath('.//span[text()="Annual Total Return (%) History"]')

        if len(h3_span_text) > 0:
            #The table we wnat is the div tag, which is a sibling to h3. The h3 and the div tag are under one overarching div tag. Get h3's sibiling
            h3 = h3_span_text[0].getparent()
            table = h3.getnext()

            #Grab all columns as lxml Element objects. This includes the 2 columns we don't want (placeholder value column + current year), so we need to filter them out.
            columns = [column for column in list(table)]

            #Assuming elements are in document order, we can just remove the first 2 elements of the list
            del columns[0:2]

            #Return filtered version
            return columns

        else:
            redirected_to_error_page = tree.xpath('.//span[contains(text(),"Symbols similar to ")]')
            if len(redirected_to_error_page) > 0:
                raise FundException.SymbolDoesNotExistError(f"Error while retrieving data for historical returns: Symbol does not exist: {fund_symbol}")
            else:
                raise FundException.UIChangedError(f"Error while retrieving data for historical returns: UI for source website of this symbol has changed, so we can't scrape the data: {fund_symbol}")


    def build_historical_return_response(self, column_data, fund_symbol):
        current_year = str(datetime.datetime.now().year)
        fund = {}
        category = {}
        response = {}

        for col in column_data:
            data = [str(span.text_content()) for span in list(col)]
            if current_year not in data and len(data) == 4:    #Grab column data for all years except current year
                #Data will be in the format of a list of 4 elements, in the order [year, ui bar, fund return, category return]. We hardcode order, as Elements are returned in document order, according to documentation
                year = int(data[0])
                fund_return_raw = data[2]
                category_return_raw = data[3]
                fund_return = "None available for current year"              #If return is "N/A", then it will have this value
                category_return = "None available for current year"

                if fund_return_raw != "N/A":
                    fund_return = float(data[2][:-1])           #Concatenate "%" off of string, then convert to float. Ex: "25.67%", we want: 25.67

                if category_return_raw != "N/A":
                    category_return = float(data[3][:-1])       #Concatenate "%" off of string, then convert to float. Ex: "25.67%", we want: 25.67

                fund[year] = fund_return
                category[year] = category_return

        response[fund_symbol] = fund
        response["Category"] = category
        return response

# import exceptions as FundException
# p = PerformanceStats()
# fund_symbol = "PRHSX"
# print(p.get_10000_growth(fund_symbol))
# print(p.get_trailing_returns(fund_symbol))
# print(p.get_fund_historical_returns(fund_symbol))
# print(p.get_performance_stats(fund_symbol))
