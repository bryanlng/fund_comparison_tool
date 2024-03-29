from bs4 import BeautifulSoup
import requests
import json
from lxml import etree, html

import fundapi.libraries.util as Util
from fundapi.libraries.util import Section
import fundapi.libraries.exceptions as FundException

class GeneralStats:
    def get_general_stats(self, fund_symbol):
        """
        Grabs general stats of the mutual fund. Grabs things:
            1. Price (NAV)
            2. Min. initial investment
            3. Expense ratio
            4. Asset allocation pie chart data(Morningstar's pie chart: Cash, US stock, Non-US stock, bonds, etc)Asset allocation pie chart data(Morningstar's pie chart: Cash, US stock, Non-US stock, bonds, etc)
            5. Morningstar overall rating
            6. Morningstar risk vs category
            7. Morningstar return vs category
            8. Morningstar category
            9. Turnover ratio
        Source = Morningstar, quotes page
        """

        response = {}
        # response["price"] = self.get_general_details(fund_symbol)
        # response["min_investment"] = self.get_asset_allocation_data(fund_symbol)
        # response["expense_ratio"] = self.get_risk_return_vs_category(fund_symbol)
        # response["asset_allocation"] = self.get_morningstar_overall_rating(fund_symbol)
        return response


    def get_general_details(self, fund_symbol):
        """
        Gets the following:
            1. Price/ NAV
            2. Minimum investment
            3. Expense ratio (in percentage, ex: .77%)
            4. Turnover ratio (in percentage, ex: .77%)
            5. Morningstar Category
        """
        # Build a dictionary, where key = time period, value = trailing return for that time period.
        response = {}
        url = Util.build_url(Section.GENERAL_STATS, fund_symbol)
        raw = requests.get(url)
        if raw.status_code == 200 and raw.text != "":
            print("200 and not empty")
            soup = BeautifulSoup(raw.text, 'html.parser')


            keys = ["NAV", "MinInvestment", "ExpenseRatio", "Turnover", "MorningstarCategory"]
            for key in keys:
                spans = soup.findAll("span", attrs={"vkey": key})
                if len(spans) > 0:
                    span = spans[0]
                    span_text = span.text
                    response[key] = span_text.strip()
                else:
                    raise FundException.UIChangedError(f"Error while retrieving data for trailing returns: UI for source website of this symbol has changed, so we can't scrape the data: {fund_symbol}")
        else:
            raise FundException.SymbolDoesNotExistError(f"Error while retrieving data for trailing returns: Symbol does not exist: {fund_symbol}")

        return response

    def get_asset_allocation_data(self, fund_symbol):
        """
        Gets the asset allocation data necessary for the pie chart
        Mimics Morningstar's asset allocation pie chart on the quotes page
        Note: On morningstar, there are 2 possible layouts:
            1. Pie chart:
                -7 rows in response (1 blank, 6 with 2 columns each: field name and value)
                -ex: PRHSX
            2. Table:
                -8 rows in response (2 irrelvant, 6 with 4 columns each: field name, net, short, long)
                -We'll only use field name and net, to match consistency with pie chart scenario
                -Contains the phrase "Note: Contains derivatives or short positions"
                -ex: FSDAX
        """
        # Build a dictionary, where key = time period, value = trailing return for that time period.
        response = {}
        url = Util.build_url(Section.ASSET_ALLOCATION, fund_symbol)
        raw = requests.get(url)
        if raw.status_code == 200 and raw.text != "":
            print("200 and not empty")
            soup = BeautifulSoup(raw.text, 'html.parser')

            fields = ["Cash", "US Stock", "US Stocks", "Non US Stock", "Non US Stocks", "Bond", "Bonds", "Other"]
            table = soup.find("table")
            if table is not None:
                rows = table.findAll(lambda tag: tag.name == 'tr')
                for row in rows:
                    rowData = [col.text for col in row.findAll("td") if col.text != ""]
                    if len(rowData) > 0:
                        fieldEntry = rowData[0]
                        if fieldEntry in fields:
                            response[fieldEntry] = rowData[1]
            else:
                raise FundException.UIChangedError(f"Error while retrieving data for trailing returns: UI for source website of this symbol has changed, so we can't scrape the data: {fund_symbol}")
        else:
            raise FundException.SymbolDoesNotExistError(f"Error while retrieving data for trailing returns: Symbol does not exist: {fund_symbol}")

        return response


    def get_risk_return_vs_category(self, fund_symbol):
        """
        Gets the:
            1. overall risk compared to its category, as judged by Morningstar
            2. overall return compared to its category, as judged by Morningstar
        Found on quotes page
        """
        response = {}
        url = Util.build_url(Section.RISK_RETURN_VS_CATEGORY, fund_symbol)
        raw = requests.get(url)
        if raw.status_code == 200 and raw.text != "":
            print("200 and not empty")
            soup = BeautifulSoup(raw.text, 'html.parser')

            fields = ["Risk vs.Category", "Return vs.Category"]
            table = soup.find("table")
            if table is not None:
                rows = table.findAll(lambda tag: tag.name == 'tr')
                for row in rows:
                    rowData = [col.text.strip() for col in row.findAll("td") if col.text.strip() != ""]
                    if len(rowData) > 0:
                        fieldEntry = rowData[0]
                        for field in fields:
                            if fieldEntry.find(field) != -1:
                                response[field] = rowData[1]
            else:
                raise FundException.UIChangedError(f"Error while retrieving data for trailing returns: UI for source website of this symbol has changed, so we can't scrape the data: {fund_symbol}")
        else:
            raise FundException.SymbolDoesNotExistError(f"Error while retrieving data for trailing returns: Symbol does not exist: {fund_symbol}")

        return response

    def get_morningstar_overall_rating(self, fund_symbol):
        """
        Gets the overall Morningstar rating
        Process:
            1. Use lxml to find the corresponding performanceId for the fund, located in head > meta name = performanceId
            2. Then, hit the security identifier API of morningstar with that id, which will return in a field the number of stars'

        Ex:
            FSDAX's performanceId is 0P00002PPP
        """
        performanceId = self.extract_performance_id(fund_symbol)

        response = {}
        url = Util.build_url(Section.OVERALL_RATING, fund_symbol, 0, performanceId)
        raw = requests.get(url)
        if raw.status_code == 200 and raw.text != "":
            print("200 and not empty")
            data = raw.json()
            if "starRating" in data:
                response["starRating"] = data["starRating"]
            else:
                raise FundException.UIChangedError(f"Error while retrieving data for trailing returns: UI for source website of this symbol has changed, so we can't scrape the data: {fund_symbol}")
        else:
            raise FundException.SymbolDoesNotExistError(f"Error while retrieving data for trailing returns: Symbol does not exist: {fund_symbol}")

        return response

    def extract_performance_id(self, fund_symbol):
        """
        Extract id from page, so get_morningstar_overall_rating() can build a url that can get the actual star rating
        """
        url = Util.build_url(Section.QUOTES_PAGE, fund_symbol)
        raw = requests.get(url)
        if raw.status_code == 200 and raw.text != "":
            #Build lxml tree from webpage
            tree = html.fromstring(raw.content)

            #Find the meta tag that says "performanceId", and extract the content field
            tags = tree.xpath('.//meta[@name="performanceId"]')
            tag = tags[0]
            return tag.get("content")
