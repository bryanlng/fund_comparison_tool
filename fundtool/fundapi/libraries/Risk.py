from bs4 import BeautifulSoup
import requests
import json

import fundapi.libraries.util as Util
from fundapi.libraries.util import Section
import fundapi.libraries.exceptions as FundException

class RiskStats:
    def get_risk_stats(self, fund_symbol):
        """
        Grabs risk stats. Grabs 8 things, for 4 time period of (3 year, 5 year, 10 year, 15 year):
            1. Alpha
            2. Beta
            3. R-squared
            4. Standard deviation
            5. Sharpe ratio
            6. Sortino ratio
            7. Treynor ratio
            8. Capture ratios (5 time periods: 1 year, 3 year, 5 year, 10 year, 15 year)
        Return in a JsonResponse encoded object
        """
        response = {}
        # response["mpt_stats"] = self.get_mpt_stats(fund_symbol)
        # response["volatility_stats"] = self.get_volatility_stats(fund_symbol)
        response["capture_ratios"] = self.get_capture_ratios(fund_symbol)
        return response


    def get_mpt_stats(self, fund_symbol):
        """
        Retrieves alpha, beta, R-squared, Treynor ratio
        """
        # Build a dictionary, where key = time period, value = trailing return for that time period.
        timespans = ["3-Year", "5-Year", "10-Year", "15-Year"]
        fields = ["Category Index", "R-Squared", "Beta", "Alpha", "Treynor Ratio", "Currency"]
        response = {}

        for timespan in timespans:
            year = timespan.split("-")[0]
            url = Util.build_url(Section.RISK_MPT, fund_symbol, year)
            raw = requests.get(url)
            if raw.status_code == 200 and raw.text != "":
                print("200 and not empty")
                soup = BeautifulSoup(raw.text, 'html.parser')

                # Find corresponding column values of trailing risk stats. These will be the values of the dict
                dataNotFoundYet = True
                table = soup.find("table")
                if table is not None:
                    rows = table.findAll(lambda tag: tag.name == 'tr')
                    for row in rows:
                        row_header = row.find("th")
                        if dataNotFoundYet and row_header != None and row_header.text == fund_symbol:
                            dataNotFoundYet = False
                            stats = [col.text.strip() for col in row.findAll("td")]
                            response[timespan] = dict(zip(fields, stats))
                else:
                    raise FundException.UIChangedError(f"Error while retrieving data for risk mpt: UI for source website of this symbol has changed, so we can't scrape the data: {fund_symbol}")
            else:
                raise FundException.SymbolDoesNotExistError(f"Error while retrieving data for risk mpt: Symbol does not exist: {fund_symbol}")

        return response

    def get_volatility_stats(self, fund_symbol):
        """
        Retrieves standard deviation, return, sharpe ratio, sortino ratio
        """
        # Build a dictionary, where key = time period, value = trailing return for that time period.
        timespans = ["3-Year", "5-Year", "10-Year", "15-Year"]
        fields = ["Standard Deviation", "Return", "Sharpe Ratio", "Sortino Ratio"]
        response = {}

        for timespan in timespans:
            year = timespan.split("-")[0]
            url = Util.build_url(Section.RISK_VOLATILITY, fund_symbol, year)
            raw = requests.get(url)
            if raw.status_code == 200 and raw.text != "":
                print("200 and not empty")
                soup = BeautifulSoup(raw.text, 'html.parser')

                # Find corresponding column values of trailing risk stats. These will be the values of the dict
                table = soup.find("table")
                if table is not None:
                    rows = table.findAll(lambda tag: tag.name == 'tr')
                    for row in rows:
                        row_header = row.find("th")
                        if row_header != None and row_header.text == fund_symbol:
                            stats = [col.text.strip() for col in row.findAll("td")]
                            del stats[len(stats)-1]                             #Remove unnecessary values
                            response[timespan] = dict(zip(fields, stats))
                else:
                    raise FundException.UIChangedError(f"Error while retrieving data for risk mpt: UI for source website of this symbol has changed, so we can't scrape the data: {fund_symbol}")
            else:
                raise FundException.SymbolDoesNotExistError(f"Error while retrieving data for risk mpt: Symbol does not exist: {fund_symbol}")

        return response

    def get_capture_ratios(self, fund_symbol):
        """
        Gets upside and downside capture ratios for 1 year, 3 year, 5 year, 10 year, 15 year
        """
        # Build a dictionary, where key = time period, value = trailing return for that time period.
        timespans = ["1-Year", "3-Year", "5-Year", "10-Year", "15-Year"]
        upsidedownside_fields = ["Upside ratio", "Downside ratio"]
        fields = ["Standard Deviation", "Return", "Sharpe Ratio", "Sortino Ratio"]
        response = {}

        url = Util.build_url(Section.CAPTURE_RATIOS, fund_symbol)
        raw = requests.get(url)
        if raw.status_code == 200 and raw.text != "":
            print("200 and not empty")
            soup = BeautifulSoup(raw.text, 'html.parser')

            # Find corresponding column values of trailing risk stats. These will be the values of the dict
            table = soup.find("table")
            if table is not None:
                rows = table.findAll(lambda tag: tag.name == 'tr')
                for row in rows:
                    row_header = row.find("th")
                    if row_header != None and row_header.text == fund_symbol:
                        stats = []
                        for col in row.findAll("td"):
                            #Values are stuck together. Ex: Convert "145.9576.71" --> "145.95", "76.71"
                            raw = col.text
                            first_dot = raw.find(".")
                            upside_ratio = raw[:first_dot+3]
                            downside_ratio = raw[first_dot+3:]
                            stats.append({"upside_ratio": upside_ratio, "downside_ratio": downside_ratio})
                        response = dict(zip(timespans, stats))
            else:
                raise FundException.UIChangedError(f"Error while retrieving data for risk mpt: UI for source website of this symbol has changed, so we can't scrape the data: {fund_symbol}")
        else:
            raise FundException.SymbolDoesNotExistError(f"Error while retrieving data for risk mpt: Symbol does not exist: {fund_symbol}")

        return response
